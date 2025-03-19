from crewai import Task
from agents import writer_agent as wr, research_agent as re
from datetime import datetime
import os
current_date = datetime.now().strftime("%Y-%m-%d-%H%M%S")


research_task = None
writer_task = None

try:
    research_task = Task(
        description= "Identify the best YT videos for the topic: {search_query}",
        expected_output= "A list of the best YT videos for the topic: {search_query}. ",
        agent=re
    )

    writer_task = Task(
        description= "Write a summary of the YT videos for the topic: {search_query}",
        expected_output= "A summary of the videos with important links and timestamps. "
        "Each summary paragraph should include the video Title and links of resources like code and datasets.",
        agent=wr,
        async_execution= False,
        output_file= f"{current_date}_Crew AI Videos Summary.md"
    )
except Exception as e:
    print(e)
finally:
    os.environ.pop('AI_MODEL', None)
    os.environ.pop('OPENAI_API_KEY', None)
    os.environ.pop('OPENAI_MODEL_NAME', None)
    os.environ.pop('HF_TOKEN', None)