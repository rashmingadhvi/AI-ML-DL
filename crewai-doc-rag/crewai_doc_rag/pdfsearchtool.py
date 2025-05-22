from crewai_tools import RagTool
import tempfile, os
from typing import Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field

# Set dummy OpenAI API key to prevent errors
os.environ["OPENAI_API_KEY"] = "dummy-key-not-used"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"

# Define the schema for the tool input
class VectorStoreSearchSchema(BaseModel):
    query: dict = Field(description="The search query or question to find information about in the PDF.")


class VectorStoreSearchTool(RagTool):
    """Tool for searching through a vector store."""
    
    name: str = "VectorStoreSearch"
    description: str = "Search for information in the embedded documents"
    args_schema: type[BaseModel] = VectorStoreSearchSchema
    
    def __init__(self, pdf_content:bytes=None):
        """Initialize the tool."""
        super().__init__()
        self._vectorstore = None
        if pdf_content:
            print(f"PDF content length = {len(pdf_content)}")
            self.add_pdf_to_embedchain(pdf_content)
    
    def _run(self, query: str) -> str:
        print("Query is: ", query)
        if isinstance(query, dict):
            if 'query' in query:
                query = query['query']
            elif 'description' in query:
                query = query['description']
            elif 'input_query' in query:
                query = query['input_query']
            else:
                query = str(query)
        try:
            if self._vectorstore:
                # Use the vectorstore with Ollama
                llm = Ollama(model="gemma3:1b")
                
                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=self._vectorstore.as_retriever(search_kwargs={"k": 3})
                )
                
                result = qa_chain.run(query)
                return result
            else:
                return "No documents have been added yet. Please add a document first."
        except Exception as e:
            return f"Error searching documents: {str(e)}"

    def add_pdf_to_embedchain(self, pdf_content):
        """Add PDF content to the vector store."""
        COLLECTION_NAME = "pdf_embeddings"
        PERSIST_DIRECTORY = "./chroma_db" 

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_content)
            temp_path = temp_file.name
        
        try:
            # Extract text from the PDF
            loader = PyPDFLoader(temp_path)
            documents = loader.load()
            
            if not documents:
                print("Warning: No text could be extracted from the PDF")
                return False
                
            print(f"Extracted {len(documents)} pages from PDF")
            
            # Create text splitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            
            # Split documents into chunks
            chunks = text_splitter.split_documents(documents)
            
            if not chunks:
                print("No chunks created, using original documents")
                chunks = documents
            
            # Create embeddings
            embeddings = OllamaEmbeddings(model="nomic-embed-text")
            
            # Create vector store
            self._vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                collection_name=COLLECTION_NAME,
                persist_directory=PERSIST_DIRECTORY,
                client_settings={"chroma_client": {"allow_reset": True}}
            )
            
            print(f"Successfully created vector store with {len(chunks)} chunks")
            return True
            
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return False
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
