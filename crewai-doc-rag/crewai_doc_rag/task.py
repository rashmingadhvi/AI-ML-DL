from crewai import Task
from agent import DocRagAgent
doc_search_task = Task(
    description="Search for relevant documents related to the user's query.",
    expected_output="The precise answer to the user's query.",
    agent=DocRagAgent
)
