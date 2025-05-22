from pdfsearchtool import VectorStoreSearchTool
import os

# Add the PDF to the tool
pdf_path = "docs/Rashmin_Gadhvi_Resume-FSD.pdf"
file_path = os.path.join(os.path.dirname(__file__), pdf_path)

with open(file_path, "rb") as f:
    pdf_content = f.read()

print(f"PDF file path = {file_path}")
print(f"PDF content length = {len(pdf_content)}")
vector_search_tool = VectorStoreSearchTool(pdf_content)
#vector_search_tool.add_pdf_to_embedchain(pdf_content)