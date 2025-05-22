from typing import Optional
from crewai_tools import RagTool
import tempfile, os
from langchain_text_splitters import CharacterTextSplitter
from pydantic import Field, model_validator
from embedchain import App
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set dummy OpenAI API key to prevent errors
os.environ["OPENAI_API_KEY"] = "dummy-key-not-used"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
pdf_path = "docs/Rashmin_Gadhvi_Resume-FSD.pdf"
class VectorStoreSearchTool(RagTool):
    """Tool for searching through a vector store."""
    
    name: str = "VectorStoreSearch"
    description: str = "Search for information in the embedded documents"
    app: Optional[App] = None
    # Configure Pydantic to allow arbitrary types
    model_config = {"arbitrary_types_allowed": True}

    def __init__(self, pdf_content: Optional[bytes] = None, **kwargs):
        """Initialize the tool with Ollama-based embedchain."""
        super().__init__(**kwargs)
       
        app_config = {
             'app': {
        'config': {
            'name': 'crewai-doc-rag-app'
        }
             },
        'llm': {
            'provider': 'ollama',
            'config': {
                'model': 'gemma3:1b',
                'base_url': os.getenv("OLLAMA_HOST", "http://localhost:11434"),
                'temperature': 0.5
            }
        },
        'embedder': {
            'provider': 'ollama',
            'config': {
                'model': 'nomic-embed-text',
                'base_url': os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            }
            
        },
        'chunker':{
                "chunk_size": 2000,
                "chunk_overlap": 50,
                "min_chunk_size": 100
            },
        'vectordb': {
            'provider': 'chroma',
                'config': {
                    'dir': './chroma_db_crewai_ollama', # Persist DB here
                    'collection_name': 'crewai-pdf-docs',
                    'allow_reset': 'true'
                }
            }
        }
            
              # Create the embedchain app with proper configuration
       
        self._setup_app(app_config)
        if pdf_content:
            self.add_pdf(pdf_content)
    
    def _setup_app(self, app_config):
        self.app = App.from_config(config=app_config)

    def _run2(self, query: str) -> str:
        """Run the tool on the given query."""
        try:
            result = self.app.query(query)
            return result
        except Exception as e:
            return f"Error searching documents: {str(e)}"

    def add_pdf(self, pdf_content: bytes, metadata: Optional[dict] = None) -> bool:
        
        if not self.app:
            print("Error: Embedchain app is not initialized.")
            return False

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(pdf_content)
                temp_path = temp_file.name
            
            print(f"Adding PDF from temporary file: {temp_path}")
            # Embedchain's add method can take metadata
            self.app.add(temp_path, metadata=metadata)
            print(f"PDF content from {temp_path} added to embedchain successfully.")
            return True
        except Exception as e:
            print(f"Error adding PDF to embedchain: {str(e)}")
            return False
        finally:
            # Clean up the temporary file
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                    print(f"Temporary file {temp_path} deleted.")
                except Exception as e:
                    print(f"Error deleting temporary file {temp_path}: {str(e)}")

    def add_pdf_to_embedchain2(self, pdf_content):
        """Add PDF content to the embedchain app."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_content)
            temp_path = temp_file.name
        
        try:
            self.app.add(temp_path)
            return True
        except Exception as e:
            print(f"Error adding PDF to embedchain: {str(e)}")
            return False
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def add_pdf_to_embedchain(self, pdf_content):
        """Add PDF content to the embedchain app."""
        
        COLLECTION_NAME = "my_pdf_embeddings"
        PERSIST_DIRECTORY = "./chroma_db_ollama" 

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
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                collection_name=COLLECTION_NAME,
                persist_directory=PERSIST_DIRECTORY
            )
            
            # Store the vectorstore in the instance for querying
            self._vectorstore = vectorstore
            
            print(f"Successfully created vector store with {len(chunks)} chunks")
            return True
            
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return False
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def _run3(self, query: str) -> str:
        """Run the tool on the given query."""
        try:
            if hasattr(self, '_vectorstore'):
                # Use the vectorstore directly
                from langchain_community.llms import Ollama
                from langchain.chains import RetrievalQA
                
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

    def _run(self, query: str) -> str:
       
        if not self.app:
            return "Error: Embedchain app is not initialized or no documents have been added."
        
        print(f"Querying embedchain with: '{query}'")
        try:
            result = self.app.query(query)
            print(f"Query result: {result}")
            return result
        except Exception as e:
            error_message = f"Error searching documents: {str(e)}"
            print(error_message)
            return error_message


# --- Example Usage (for testing the tool directly) ---
if __name__ == '__main__':
    print("Starting VectorStoreSearchTool Test...")
    print("Ensure Ollama server is running and models (nomic-embed-text, gemma:2b or your LLM) are pulled.")

    dummy_pdf_content = None
    
    try:
            
            file_path = os.path.join(os.path.dirname(__file__), pdf_path)
            with open(file_path, "rb") as f:
                dummy_pdf_content = f.read()
    except FileNotFoundError:
             print("Test PDF file not found.")
    
    if dummy_pdf_content:
        print("\nInitializing VectorStoreSearchTool...")
        search_tool = None # Define search_tool here to access it in except block
        try:
            search_tool = VectorStoreSearchTool() # Initialize the tool
    
            if not search_tool.app: # Check if app initialization failed
                raise Exception("Tool initialization failed: Embedchain app (self.app) is None.")

            print("\nAdding PDF to the tool...")
            # Alternatively, pass at init: search_tool = VectorStoreSearchTool(pdf_content=dummy_pdf_content)
            metadata_example = {"source_filename": "dummy_test.pdf", "creation_date": "2024-05-21"}
            success_add = search_tool.add_pdf(dummy_pdf_content, metadata=metadata_example)
            
            if success_add:
                print("\nPDF added (or processed). Now running test queries...")
                
                test_queries = [
                    "What is this document about?",
                    "What job role is this applied for?",
                    "Tell me what phone number is mentioned to call." # Should yield "No relevant information"
                ]

                for i, current_query in enumerate(test_queries):
                    print(f"\n--- Test Query {i+1} ---")
                    answer = search_tool._run(current_query) # Use _run as CrewAI would
                    print(f"Q: {current_query}\nA: {answer}")
            else:
                print("Failed to add PDF to the tool. Cannot proceed with queries.")
                print("Please check console output for errors during app initialization or PDF addition.")

        except Exception as e:
            print(f"\n--- AN UNEXPECTED ERROR OCCURRED DURING THE TEST ---")
            print(f"Error: {e}")
            print("\nTroubleshooting Checklist:")
            print("1. Is your Ollama server running? (e.g., `ollama serve` in terminal if not a service)")
            print("2. Are the Ollama models ('nomic-embed-text', 'gemma:2b' or your specified LLM) pulled? (`ollama list`)")
            print("3. Review all console output above for specific error messages from embedchain or Ollama.")
            db_dir_path = './chroma_db_crewai_ollama_tool'
            if search_tool and search_tool.app and hasattr(search_tool.app.db, 'config') and hasattr(search_tool.app.db.config, 'dir'):
                 db_dir_path = search_tool.app.db.config.dir
            print(f"4. Is the ChromaDB directory ('{db_dir_path}') writable by the script? Check its contents.")
            print("5. If 'allow_reset' is True, data is cleared on each init. Ensure `add_pdf` is called *after* init for the current instance.")

    else:
        print("\nNo PDF content was available for testing. Please ensure ReportLab is installed or provide a test PDF.")