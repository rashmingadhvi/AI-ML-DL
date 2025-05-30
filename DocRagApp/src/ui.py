import tempfile

from crewai import LLM, Agent, Crew, Process, Task
from langchain_community.llms import Ollama
from tool import create_vector_search_tool
import streamlit as st
from streamlit_elements import elements, mui, html
from DocRagCrew import DocRagCrew
import os

os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OLLAMA_HOST"] = "http://localhost:11434"
uploadedFile = None

def onClickRun():
        st.session_state.messages.append(
                {"role": "user", "content": st.session_state.chat_input}
        )
        return


def create_agents_and_tasks(pdf_tool):
    
    #llm = OllamaLLM(
     #   model="ollama/gemma3:1b",
      #  base_url="http://localhost:11434"
    #)
    #from crewai import LLM
    
    llm = LLM(
    model="ollama/llama3:8b",
    base_url="http://localhost:11434",
    api_key="sk-111111111111111111111111111111111111111111111111",
    provider="openai"
        )

    retriever_agent = Agent(
        role="Retrieve relevant information to answer the user query: {query}",
        goal=(
            "Retrieve the most relevant information from the available sources "
            "for the user query: {query}. Always try to use the PDF search tool first. "
            "If you are not able to retrieve the information from the PDF search tool, "
            "then try to use the web search tool."
        ),
        backstory=(
            "You're a meticulous analyst with a keen eye for detail. "
            "You're known for your ability to understand user queries: {query} "
            "and retrieve knowledge from the most suitable knowledge base."
        ),
        verbose=True,
        tools=[t for t in [pdf_tool] if t],
        llm=llm
    )

    response_synthesizer_agent = Agent(
        role="Response synthesizer agent for the user query: {query}",
        goal=(
            "Synthesize the retrieved information into a concise and coherent response "
            "based on the user query: {query}. If you are not able to retrieve the "
            'information then respond with "I\'m sorry, I couldn\'t find the information '
            'you\'re looking for."'
        ),
        backstory=(
            "You're a skilled communicator with a knack for turning "
            "complex information into clear and concise responses."
        ),
        verbose=True,
        llm=llm
    )

    retrieval_task = Task(
        description=(
            "Retrieve the most relevant information from the available "
            "sources for the user query: {query}"
        ),
        expected_output=(
            "The most relevant information in the form of text as retrieved "
            "from the sources."
        ),
        agent=retriever_agent
    )

    response_task = Task(
        description="Synthesize the final response for the user query: {query}",
        expected_output=(
            "A concise and coherent response based on the retrieved information "
            "from the right source for the user query: {query}. If you are not "
            "able to retrieve the information, then respond with: "
            '"I\'m sorry, I couldn\'t find the information you\'re looking for."'
        ),
        agent=response_synthesizer_agent
    )

    crew = Crew(
        agents=[retriever_agent, response_synthesizer_agent],
        tasks=[retrieval_task, response_task],
        process=Process.sequential,  # or Process.hierarchical
        verbose=True
      
    )
    return crew

container = st.sidebar.container()


if "messages" not in st.session_state:
    st.session_state.messages = []  # Chat history

if "pdf_tool" not in st.session_state:
    st.session_state.pdf_tool = None  # Store the PDFSearchTool


if "crew" not in st.session_state:
    st.session_state.crew = None  

with container:

        with elements("sidebar"):
                with mui.Accordion(defaultExpanded=True, expandIcon="ArrowDownwardIcon"):
                        with mui.AccordionSummary():
                                mui.Typography("Model Parameters")
                                with mui.AccordionDetails():
                                        st.session_state.temperature = mui.TextField(label="Temperature", defaultValue="0.1", variant="outlined")
                                        st.session_state.maxtokens = mui.TextField(label="Max Tokens", defaultValue="100", variant="outlined")
                                        mui.TextField(label="Context Window", defaultValue="1000", variant="outlined")    

                with mui.Accordion(defaultExpended=True, expandIcon="ArrowDownwardIcon"):
                        with mui.Card():
                                with mui.CardContent():
                                        st.markdown("### Chat with your file")
                                        st.session_state.modelname = st.text_area("Model Name", height=100)
                                        st.button("Run", on_click=onClickRun)
                                        uploadedFile = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])

                with elements("dat"):
                        with mui.Paper(elevation=3, style={"padding": "20px", "margin": "20px"}):
                                mui.Typography("Chat with your file", variant="h5")
                                mui.Typography("TBD", variant="body1")

                if uploadedFile is not None:
                         if st.session_state.pdf_tool is None:
                                # Save the file to a temporary location
                                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                                temp_file.write(uploadedFile.getvalue())
                                temp_file.close()
                                
                                # Import directly
                                from pdfsearchtool import VectorStoreSearchTool
                                
                                # Create the tool with the PDF content
                                with open(temp_file.name, "rb") as f:
                                        pdf_content = f.read()
                                
                                # Create the tool
                                st.session_state.pdf_tool = VectorStoreSearchTool(pdf_content)
                                st.success("PDF indexed! Ready to chat.")
               
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Write a questions about the PDF")

if prompt is not None:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
                st.markdown(prompt)
       
      
        if st.session_state.crew is None:
                #st.session_state.crew = DocRagCrew(st.session_state.pdf_tool, uploadedFile.name).crew()
                 st.session_state.crew = create_agents_and_tasks(st.session_state.pdf_tool)
        """if st.session_state.crew is not None:
                appinputs = dict({
                'input_query': prompt
                })
                result= st.session_state.crew.kickoff(inputs=appinputs)
                st.session_state.messages.append({"role": "assistant", "content": result})
        else:
                st.error("Crew not initialized")
                st.stop()
        """
        with st.chat_message("assistant"):
                st.markdown("Thinking...")
                
                inputs = {"query": prompt}
                result = st.session_state.crew.kickoff(inputs=inputs).raw
                st.markdown(result)
                st.session_state.messages.append({"role": "assistant", "content": result})        