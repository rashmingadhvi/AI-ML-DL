from crewai import Agent, LLM
from tool import vector_search_tool
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
    llm=LLM( model="ollama/gemma3:1b", 
    base_url="http://localhost:11434")
    #ChatOpenAI(model="gemma3:1b", temperature=0.2, base_url="http://localhost:11434"),
   
     
    @agent
    def rag_agent(self) -> Agent:
        # Make sure the tool has the PDF loaded
        if not hasattr(vector_search_tool, '_vectorstore') or vector_search_tool._vectorstore is None:
            # Load the PDF if not already loaded
            pdf_path = os.path.join(os.path.dirname(__file__), "docs/Rashmin_Gadhvi_Resume-FSD.pdf")
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    pdf_content = f.read()
                vector_search_tool.add_pdf_to_embedchain(pdf_content)
                print(f"Loaded PDF from {pdf_path}")
            else:
                print(f"Warning: PDF file not found at {pdf_path}")
        
        return Agent(
            config=self.agents_config['DocRagAgent'],
            verbose=True,
            tools=[vector_search_tool],
            llm=self.llm,
            max_iterations=5
        )

    @task
    def doc_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['doc_search_task'],
            agent=self.rag_agent(),
            output_file="./output_1.txt"
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
     