from crewai import Agent, LLM
from crewai_tools import RagTool
from langchain_openai import ChatOpenAI
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import logging, os
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



@CrewBase
class DocRagCrew:
    agents_config = 'config/agent_config.yaml'
    tasks_config = 'config/task_config.yaml'
    in_file='input.txt'
    out_file='output.txt'
    url = os.getenv("OLLAMA_HOST")
    name = f"ollama/{os.getenv('OLLAMA_MODEL')}"

   
    #llm=ChatOpenAI(model="ollama/gemma3:1b", temperature=0.7, provider= "ollama", base_url="http://localhost:11434", streaming= False)

    def __init__(self, tool: RagTool, fileName: str= None) -> None:
        self.tool = tool
        if fileName is None:
            fileName = ""
        else:
            fileName = fileName
        self.fileName = fileName
        url = os.getenv("OLLAMA_HOST")
        name = "ollama/"+os.getenv("OLLAMA_MODEL")
        #print(f"Initialized DocRagCrew with tool: {tool} and fileName: {fileName}")
        self.llm = LLM(
            model=name, 
            base_url=url,
            stream=False,
            verbose=True
        )
    
    @agent
    def rag_agent(self) -> Agent:
        # Make sure the tool has the PDF loaded
        if not hasattr(self.tool, '_vectorstore') or self.tool._vectorstore is None:
            
            if self.tool._vectorstore is None and self.fileName is not None and self.fileName is not "":
                # Load the PDF if not already loaded
                pdf_path = os.path.join(os.path.dirname(__file__), self.fileName)
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        pdf_content = f.read()
                    self.tool.add_pdf_to_embedchain(pdf_content)
                    print(f"Loaded PDF from {pdf_path}")
                else:
                    print(f"Warning: PDF file not found at {pdf_path}")
        
        return Agent(
            config=self.agents_config['DocRagAgent'],
            verbose=True,
            tools=[self.tool],
            llm=self.llm
        )

   
    @task
    def retrieval_task(self) -> Task:
        return Task(
			config=self.tasks_config['retrieval_task'],
			verbose=True
		)
    @task
    def response_task(self) -> Task:
        return Task(
			config=self.tasks_config['response_task'],
			verbose=True
		)
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True, 
            output_log_file="./op.log"
        )