from crewai import Agent, LLM
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from huggingface_hub import login
import os
from langchain.llms import HuggingFaceHub, HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings 

research_agent = None
writer_agent = None

try:
    hftoken = os.getenv('HF_TOKEN')
    model_name = os.getenv('AI_MODEL')
    login(token=hftoken)
    
    crewaimodel_name = f"huggingface/{model_name}"   
  
    
  
    research_agent = Agent(
        name='Research Agent',
        role='Sr Researcher',
        goal= "Get YT videos for the topic: {search_query}",
        memory = True,
        verbose = False,
        allow_delegation= False,
        backstory="You are a expert reachers with a lot of experience in the field of {search_query}. "
        "You have been asked to find some YT videos on the topic and find the gyst of the videos and write a summary of "
        "the videos with important links and timestamps. Videos should have viewer rating 4.5 or above.",
         llm=LLM(model=crewaimodel_name, api_key=hftoken) 

    )

    writer_agent = Agent(
        name='Writer Agent',
        role='Sr Content Writer',
        goal= "Write a summary of the YT videos for the topic: {search_query}",
        memory = True,
        verbose = False,
        allow_delegation= False,
        backstory="You are an expert writer with a lot of experience in the field of {search_query}. "
        "You have been asked to write a summary of the videos subject: {search_query} with important links and timestamps."
        "Videos should have viewer rating 4.5 or above. Write the model name below title of file.",
        llm=LLM(model=crewaimodel_name, api_key=hftoken) 

    )

except Exception as e:
    print(e)
finally:
    os.environ.pop('AI_MODEL', None)
    os.environ.pop('OPENAI_API_KEY', None)
    os.environ.pop('OPENAI_MODEL_NAME', None)
    os.environ.pop('HF_TOKEN', None)