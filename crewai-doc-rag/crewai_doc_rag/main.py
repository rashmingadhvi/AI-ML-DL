from DocRagCrew import DocRagCrew
import logging, os
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
try:
    with open(file_path, 'r') as f:
        input_text = f.read()
except FileNotFoundError:
    print(f"Error: Could not find {file_path}")
    exit(1)

inputs = dict({
          'input_query': input_text
    })
result= DocRagCrew().crew().kickoff(inputs=inputs)

print("\n\n########################")
print("## Here is the result")
print("########################\n")
print(result)

""" DocRageAgent = lambda: Agent(
    role="DocRag Agent",
    goal="Answer the questions from documents of the DocRag project.",
    backstory="You are a helpful assistant that answers questions about the documentation of the DocRag project.",
    tools=[pdf_tool],
    llm=ChatOpenAI(model="gemma3:1b", temperature=0.2, base_url="http://localhost:11434"),
    max_iterations=5
) """  
