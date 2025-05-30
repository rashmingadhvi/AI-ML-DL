from crewai import LLM
from crewai_tools import RagTool
import tempfile, os
from typing import Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM
from pydantic import BaseModel, Field
from chromadb.config import Settings

# Set dummy OpenAI API key to prevent errors
os.environ["OPENAI_API_KEY"] = "dummy-key-not-used"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434"
os.environ["OLLAMA_HOST"] = "http://localhost:11434"
os.environ["OLLAMA_MODEL"] = "llama3.2:1b"


# Define the schema for the tool input
class VectorStoreSearchSchema(BaseModel):
    query: dict = Field(...,description="The search query or question to find information about in the PDF or document text.")


class VectorStoreSearchTool(RagTool):
    
    
    name: str = "VectorStoreSearch"
    description: str = "Search for information in the embedded documents"
    args_schema: type[BaseModel] = VectorStoreSearchSchema
    
    def __init__(self, pdf_content:bytes=None):
        
        super().__init__()
        self._vectorstore = None
        if pdf_content:
           self.add_pdf_to_embedchain(pdf_content)

    def extract_query(self, query: str) -> str:
         actual_query = None
         if isinstance(query, dict):
                # Try to extract the actual query from various possible keys
                for key in ['input_query', 'query', 'description']:
                    if key in query and query[key] and not isinstance(query[key], dict):
                        actual_query = query[key]
                        break
                
                # If we still don't have a query, check if 'query' is a dict with nested values
                if not actual_query and 'query' in query and isinstance(query['query'], dict):
                    for key in ['input_query', 'text', 'question']:
                        if key in query['query']:
                            actual_query = query['query'][key]
                            break
         else:
                actual_query = query
    
         return str(actual_query) if actual_query is not None else "-->No query provided"
    
    def _run(self, query: str) -> str:
        print("Query is: ", query)
        actual_query = self.extract_query(query)
        if not actual_query or actual_query == "The search query or question to find information about in the PDF.":
            return "You didn't provide a specific question. Please ask a question about the document."
    
        try:
            if self._vectorstore:
                llm = OllamaLLM(
                    model=os.getenv("OLLAMA_MODEL"),
                    base_url=os.getenv("OLLAMA_HOST")
                )
                from langchain.prompts import PromptTemplate
            
                template = """
                Answer the following question based on the context provided:
                Context: {context}
                Question: {question}
                Answer:
                """
                prompt = PromptTemplate(
                    template=template,
                    input_variables=["context", "question"]
                )
                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=self._vectorstore.as_retriever(search_kwargs={"k": 3}),
                    chain_type_kwargs={"prompt": prompt}
                )
                
                result = qa_chain.invoke({"query": actual_query})
                print("Result is: ", result)
                if isinstance(result, dict) and 'result' in result:
                    return result['result']
                elif isinstance(result, str):
                    return result
                else:
                    return str(result)
            else:
                return "No documents have been added yet. Please add a document first."
        except Exception as e:
            return f"Error searching documents: {str(e)}"

    def add_pdf_to_embedchain(self, pdf_content):
        
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
            
            embeddings = OllamaEmbeddings(model="nomic-embed-text")
           
            self._vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                collection_name=COLLECTION_NAME,
                persist_directory=PERSIST_DIRECTORY,
                client_settings=Settings(allow_reset= True, anonymized_telemetry=False, is_persistent=True)
            )
            
            return True
            
        except Exception as e:
            print(f"{self.name}->Error processing PDF: {str(e)}")
            return False
        finally:
           if os.path.exists(temp_path):
                os.unlink(temp_path)
