from crewai import Agent
from tool import vector_search_tool
DocRagAgents = Agent(
    role="DocRag Agent",
    goal="Answer the questions from documents of the DocRag project.",
    backstory="You are a helpful assistant that answers questions about the documentation of the DocRag project.",
    tools=[vector_search_tool],
    max_iterations=2
)