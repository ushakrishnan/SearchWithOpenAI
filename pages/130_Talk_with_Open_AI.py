#!/usr/bin/env python3
# Import os to set API key
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory, ConversationBufferMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from langchain.callbacks import get_openai_callback
from common.funs import get_conversation_string
from st_pages import add_indentation
from dotenv import load_dotenv
# Load default environment variables (.env)
load_dotenv()

styl = "<style>.row-widget.stTextInput{position: fixed; bottom: 3rem;}</style>"

st.markdown(styl, unsafe_allow_html=True)

add_indentation()

openai_api_key = os.environ["OPENAI_API_KEY"] = os.environ["OAI_OPENAI_API_KEY"]

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

if 'buffer_memory' not in st.session_state:
    memory = st.session_state.buffer_memory=ConversationBufferWindowMemory(return_messages=True, k=5)

with st.sidebar:
    systemInstruction = st.text_area(height=150 , label="Temper response from ChatGPT", value="Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say 'I don't know'")

system_msg_template = SystemMessagePromptTemplate.from_template(template=systemInstruction)

human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()

with textcontainer:
    prompt = st.text_input("Let's talk:", key="input", placeholder="Let's start, type here . . . ")
    if prompt:
        with get_openai_callback() as cb:
            conversation_string = get_conversation_string()
            response = conversation.predict(input=prompt)
            st.write(cb)
        st.session_state.requests.append(prompt)
        st.session_state.responses.append(response) 
with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')