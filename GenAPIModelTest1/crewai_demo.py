from crewai import Crew, Process
from agents import research_agent, writer_agent
from tasks import research_task, writer_task
from dotenv import load_dotenv, unset_key
import os
import ssl

try:

    load_dotenv()

    print("AI_MODEL = ", os.getenv('AI_MODEL'))

    os.environ['AI_MODEL']=os.getenv('AI_MODEL')
    os.environ['OPENAI_API_KEY']=os.getenv('OPENAI_API_KEY')
    os.environ['OPENAI_MODEL_NAME']=os.getenv('OPENAI_MODEL_NAME')
    os.environ['HF_TOKEN']=os.getenv('HF_TOKEN')



    crew_demo = Crew(
        name='Crew AI Demo 1 - RMK',
        agents=[research_agent, writer_agent],
        process= Process.sequential,
        tasks=[research_task, writer_task],
        memory=True,
        cache=True,
        verbose=False,
        max_rpm=100,
        share_crew=True
        
    )

    result = crew_demo.kickoff(inputs={'search_query': 'Crew AI Tutorials', 'model_name': os.getenv('AI_MODEL')})
except Exception as e:
    print(e)
finally:
    os.environ.pop('AI_MODEL', None)
    os.environ.pop('OPENAI_API_KEY', None)
    os.environ.pop('OPENAI_MODEL_NAME', None)
    os.environ.pop('HF_TOKEN', None)