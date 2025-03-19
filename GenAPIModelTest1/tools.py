from crewai_tools import YoutubeVideoSearchTool, YoutubeChannelSearchTool
import os
ytv_tool = None
try:
    ytv_tool= YoutubeVideoSearchTool(search_videos=True, search_channels=False, search_query="CewAI Tutorials", max_results=10) 

    def search_videos(query):
        # Perform the search
        results = ytv_tool.search(query)
        
        # Print the results
        for result in results:
            print(f"Title: {result['title']}")
            print(f"URL: {result['url']}")
            print(f"Description: {result['description']}")
            print("===================================")

except Exception as e:
    print(e)
finally:
    
    os.environ.pop('AI_MODEL', None)
    os.environ.pop('OPENAI_API_KEY', None)
    os.environ.pop('OPENAI_MODEL_NAME', None)
    os.environ.pop('HF_TOKEN', None)