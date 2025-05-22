from crewai import LLM, Crew, Task, Agent, Process
from crewai_tools import PDFSearchTool
from agent import DocRagAgents as agent_instance
from task import doc_search_task as task_instance
class DocRag:

    def __init__(self, name):
        self.name = name
        llm=LLM( model="ollama/gemma3:1b", 
        base_url="http://localhost:11434")
        self.crew = Crew(
            agents=[self.__get_agent__()],
            tasks=[self.__get_task__()],
            process=Process.hierarchical,
            verbose=True,
            manager_llm=llm
        )

    __get_agent__ = lambda self: agent_instance
    __get_task__ = lambda self: task_instance
    def __run__(self):
        crewop = self.crew.kickoff(dict(input="what is  number to call?"))
        print(crewop)
        
    

doc_rag = DocRag(name="Document Rag App")
doc_rag.__run__()
