import base64
import streamlit as st
from streamlit_elements import elements, mui, html

import os
st.session_state.messages= []
st.session_state.messages.append({"role": "assistant", "content": "How can I help you?"})


file_path = os.path.join(os.path.dirname(__file__), '../output_1.txt')
#st.markdown("file path = "+file_path)
result = ""
try:
        with open(file_path, 'r') as f:
            result = f.read()
except FileNotFoundError:
        result = f"Error: Could not find {file_path}"
        exit(1)
uploadedFile = None

def onClickRun():
        st.session_state.messages.append(
                {"role": "user", "content": st.session_state.chat_input}
        )
        return

container = st.sidebar.container()



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
                                mui.Typography(result, variant="body1")


for msg1 in st.session_state.messages:
        usermsg = st.chat_message("user")
        aimsg = st.chat_message("assistance")
        if msg1["role"] == "user":
                usermsg.write(msg1["content"])
        else:
                aimsg.write(msg1["content"])

