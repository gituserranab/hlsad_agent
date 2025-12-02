import streamlit as st
from google import genai
from google.genai.errors import APIError
from pypdf import PdfReader
import io
import os

#from streamlit_ngrok import ngrok
#import streamlit as st

#ngrok.connect(port='8501')


# In app.py, change:
# client = genai.Client()

# TO:
client = genai.Client(api_key="AIzaSyBKupnUpF6bk79INhuIwAR2AlJBZzsVzLA")

# gemini_api_key = "AIzaSyBKupnUpF6bk79INhuIwAR2AlJBZzsVzLA"


# 1. & 3. Document Analysis Function
def analyze_document(file_bytes):
    try:
        # Initialize the client using the environment variable
        client = genai.Client()

        # Read the uploaded PDF file
        reader = PdfReader(io.BytesIO(file_bytes))
        document_text = ""
        for page in reader.pages:
            document_text += page.extract_text()
        
        # Craft the prompt for analysis
        prompt = (
            "Analyze the following system document content. "
            "Identify areas for improvement regarding clarity, completeness, integration, api changes if mentioned, interface specification, structure, and adherence to best practices for a system document. "
            "Provide your comments clearly, referencing specific sections or topics. "
            "Finally, provide a single revised version of the document with improvements incorporated. "
            "Use clear headings for: 1. Improvement Comments and 2. Revised Document."
            "\n\n--- DOCUMENT CONTENT ---\n" + document_text
        )

        # Call the Gemini model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except APIError as e:
        return f"An API Error occurred: {e}. Check your API Key and quota."
    except Exception as e:
        return f"An error occurred: {e}. Ensure the file is a valid PDF."

# 5. Simple GUI using Streamlit
st.title("📄 AI System Document Review Agent PoC")
st.markdown("Upload your system document template (PDF) for AI-driven improvement comments and a revised draft.")

# 2. File Upload
uploaded_file = st.file_uploader("Choose a PDF Document", type="pdf")

if uploaded_file is not None:
    st.info("Document uploaded successfully. Analyzing...")
    
    # Process the file
    file_bytes = uploaded_file.getvalue()
    analysis_result = analyze_document(file_bytes)
    
    st.subheader("✅ Analysis Complete")
    st.markdown(analysis_result)
    
    # 4. Download Reviewed Document (Simplification for PoC)
    # The PoC provides the "Revised Document" text directly in the output.
    # To enable download, we create a simple text file from the result.
    st.download_button(
        label="Download Analysis and Revised Document (Text File)",
        data=analysis_result,
        file_name="reviewed_document_and_comments.txt",
        mime="text/plain"
    )

st.caption("Powered by Gemini 2.5 Flash and Streamlit.")
