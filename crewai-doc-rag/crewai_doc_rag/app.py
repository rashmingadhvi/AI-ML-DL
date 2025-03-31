from multiprocessing import Process
from crewai import Crew, Task, Agent
from crewai_tools import PDFSearchTool
from agent import DocRageAgents
from task import doc_search_task
class DocRag:

    def __init__(self, name):
        self.name = name
        self.crew = Crew(
            agents=[self.__get_agent__()],
            tasks=[self.__get_task__()],
            process=Process.hierarchical,
            verbose=2,
        )

    __get_agent__: lambda self: DocRageAgents()
    __get_task__: lambda self: doc_search_task()
    def __run__(self):
        crewop = self.crew.kickoff()
        print(crewop.json(indent=2))
        
    

doc_rag = DocRag()
doc_rag.__run__()
