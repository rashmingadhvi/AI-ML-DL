from crewai import Task
from agent import DocRagAgents
doc_search_task = Task(
  description= "Search for information in the PDF document",
  expected_output= "Relevant information from the document",
  agent= DocRagAgents,
  context= "Use the VectorStoreSearch tool to find information in the document.")
