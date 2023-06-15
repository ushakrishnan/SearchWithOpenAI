#!/usr/bin/env python3
# Import os to set API key
import os
# Import OpenAI as main LLM service
from langchain.llms import AzureOpenAI, openai
from langchain.callbacks import get_openai_callback
# Bring in streamlit for UI/app interface
import streamlit as st
from st_pages import add_indentation
from dotenv import load_dotenv
from common.funs import getfromkusto

# Import vector store stuff
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo
)
# Load default environment variables (.env)
load_dotenv()

add_indentation()

# Set this to `azure`
openai_api_type = os.environ["OPENAI_API_TYPE"] = "azure"
openai_api_base = os.environ["OPENAI_API_BASE"] = os.environ["AOAI_OPENAI_API_BASE"]
openai_api_key = os.environ["OPENAI_API_KEY"] = os.environ["AOAI_OPENAI_API_KEY"]

openai_model =  os.environ["AOAI_OPENAI_API_COMP_MODEL"]
openai_api_version = os.environ["AOAI_OPENAI_API_COMP_VERSION"]

# Create instance of OpenAI LLM
llm = AzureOpenAI(openai_api_base=openai_api_base , model=openai_model, temperature=0.1, verbose=True, deployment_name=openai_model, openai_api_key=openai_api_key)  # noqa: E501


st.title("🦜🔗🤗 What would you like to know?")
st.write("This sample uses **Azure OpenAI for Encoding & Search, Azure Cognitive Services for document storage and retrieval, and Kusto as vector datastore (including cosine similarity search as Kusto function)**")  # noqa: E501
# Create a text input box for the user
prompt = st.text_input('Input your prompt here:')

# If the user hits enter
if len(prompt) > 0:
    with get_openai_callback() as cb:
        try:
            # Then pass the prompt to the LLM
            store = getfromkusto(prompt + " and stop when you know the answer")

            prompt_template = f"""Use the following pieces of context to answer the question at the end. Use all content and summarize response with all possible answers. write the response as a full sentence in about 100 words. If you don't know the answer, just say that you don't know, don't try to make up an answer.
                {store}
                Question: {prompt}
                Answer:"""
            print(prompt_template)

            completion = openai.completion_with_retry(deployment_id=openai_model, prompt=prompt_template, temperature=1, llm=llm)
            # ...and write it out to the screen
            st.write(completion)
            st.write(cb)
        except Exception as e:
            st.warning(e)
            st.write("That was a difficult question!  I choked on it!!  Can you please try again with rephrasing it a bit?")
            st.write(cb)
            print(e)
else:
    st.write("Why don't you add your question in the textbox and press enter to test me?")
