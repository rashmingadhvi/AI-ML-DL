import tempfile
import streamlit as st
from streamlit_elements import elements, mui, html
import os
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from DocRagCrew import DocRagCrew
from pdfsearchtool import VectorStoreSearchTool

os.environ["OPENAI_API_KEY"] = "dummy-key-not-used"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434"
os.environ["OLLAMA_HOST"] = "http://localhost:11434"
os.environ["OLLAMA_MODEL"] = "llama3.2:1b"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []  # Chat history

if "pdf_tool" not in st.session_state:
    st.session_state.pdf_tool = None  # Store the PDFSearchTool

if "crew" not in st.session_state:
    st.session_state.crew = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# UI components
st.title("PDF Question Answering")

def extract_result(response:str)->str:
    
    if hasattr(response, 'raw'):
        result = response.raw
    elif isinstance(response, dict) and 'result' in response:
        result = response['result']
    elif isinstance(response, str):
        result = response
    else:
        # Try to extract from the string representation
        import re
        response_str = str(response)
        match = re.search(r"'result':\s*'([^']*)'", response_str)
        if match:
            result = match.group(1)
        else:
            result = response_str
    print("Extracted Result is: ", result)
    return result        

with st.sidebar:
    st.header("Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.slider("Max Tokens", 100, 2000, 1000)
    
    # File uploader
    st.session_state.uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    
    if st.session_state.uploaded_file  is not None:
        with st.spinner("Processing PDF..."):
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_file.write(st.session_state.uploaded_file.getvalue())
            temp_file.close()
            
            with open(temp_file.name, "rb") as f:
                pdf_content = f.read()
            
            pdf_tool = VectorStoreSearchTool(None)
            success = pdf_tool.add_pdf_to_embedchain(pdf_content)
        
            if success:
                st.session_state.pdf_tool = pdf_tool
                if st.session_state.crew is None:
                    st.session_state.crew = DocRagCrew(st.session_state.pdf_tool, temp_file.name).crew()
                st.success("PDF processed successfully!")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask a question about the PDF")

if prompt:
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    if st.session_state.pdf_tool is None or st.session_state.crew is None:
        with st.chat_message("assistant"):
            st.error("Please upload a PDF first.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.crew.kickoff(inputs={"query": prompt})
                    result = extract_result(response);
                    st.markdown(result)
                    st.session_state.messages.append({"role": "assistant", "content": result})
                except Exception as e:
                    st.error(f"Error: {str(e)}")