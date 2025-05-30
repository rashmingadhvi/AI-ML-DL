import tempfile
import streamlit as st
from streamlit_elements import elements, mui, html
import os
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Import your VectorStoreSearchTool
from pdfsearchtool import VectorStoreSearchTool

os.environ["OPENAI_API_BASE"] = "http://localhost:11434"
os.environ["OLLAMA_HOST"] = "http://localhost:11434"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []  # Chat history

if "pdf_tool" not in st.session_state:
    st.session_state.pdf_tool = None  # Store the PDFSearchTool

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

# UI components
st.title("PDF Question Answering")

# Sidebar
with st.sidebar:
    st.header("Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.slider("Max Tokens", 100, 2000, 1000)
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    
    if uploaded_file is not None and st.session_state.pdf_tool is None:
        with st.spinner("Processing PDF..."):
            # Save the file to a temporary location
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_file.write(uploaded_file.getvalue())
            temp_file.close()
            
            # Create the tool with the PDF content
            with open(temp_file.name, "rb") as f:
                pdf_content = f.read()
            
            # Create the tool
            st.session_state.pdf_tool = VectorStoreSearchTool(pdf_content)
            
            # Create the QA chain
            if st.session_state.pdf_tool._vectorstore:
                llm = Ollama(
                    model="gemma3:1b",
                    base_url="http://localhost:11434",
                    temperature=temperature
                )
                
                template = """
                Answer the question based on the context provided.
                
                Context: {context}
                
                Question: {question}
                
                Answer:
                """
                
                prompt = PromptTemplate(
                    template=template,
                    input_variables=["context", "question"]
                )
                
                st.session_state.qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=st.session_state.pdf_tool._vectorstore.as_retriever(search_kwargs={"k": 3}),
                    chain_type_kwargs={"prompt": prompt}
                )
                
            st.success("PDF processed successfully!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask a question about the PDF")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Check if PDF is loaded
    if st.session_state.qa_chain is None:
        with st.chat_message("assistant"):
            st.error("Please upload a PDF first.")
    else:
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.qa_chain.run(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {str(e)}")
