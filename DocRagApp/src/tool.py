from pdfsearchtool import VectorStoreSearchTool
import os


def create_vector_search_tool(fileURI:str) -> VectorStoreSearchTool:
    file_path = os.path.join(os.path.dirname(__file__), fileURI)
    with open(file_path, "rb") as f:
        pdf_content = f.read()

    print(f"PDF file path = {file_path}")
    print(f"PDF content length = {len(pdf_content)}")
    return VectorStoreSearchTool(pdf_content)

