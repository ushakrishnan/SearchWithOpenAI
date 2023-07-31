# Import os to set API key
import os
import langchain

# Bring in streamlit for UI/app interface
import streamlit as st

from langchain.callbacks import get_openai_callback
from langchain.utilities import GoogleSerperAPIWrapper
from common.SerperSearchRetriever import SerperSearchRetriever
from st_pages import add_indentation
from dotenv import load_dotenv
from langchain.chains import FlareChain
from langchain.llms.openai import OpenAI

langchain.verbose = True

# Load default environment variables (.env)
load_dotenv()

add_indentation()

openai_api_type = os.environ["OPENAI_API_TYPE"] ="open_ai"
openai_api_version = os.environ["OPENAI_API_VERSION"] = os.environ["OAI_OPENAI_API_VERSION"]
openai_api_base = os.environ["OPENAI_API_BASE"] = os.environ["OAI_OPENAI_API_BASE"]
openai_api_key = os.environ["OPENAI_API_KEY"] = os.environ["OAI_OPENAI_API_KEY"]
serper_api_key = os.environ["SERPAPI_API_KEY"]

st.title("🦜🔗🤗 What would you like to know?")
st.write("This sample uses **OpenAI and Serper**")

llm = OpenAI(temperature=0.1, verbose=True, model="text-davinci-002", openai_api_base=openai_api_base,  openai_api_key=openai_api_key )

# Create a text input box for the user
prompt = st.text_input('Input your prompt here: ex. what are the ingredients for fortify alchemy potion')

# If the user hits enter
if len(prompt) > 0:
    with get_openai_callback() as cb:
        try:
            retriever = SerperSearchRetriever(search=GoogleSerperAPIWrapper())
            flare = FlareChain.from_llm(llm, retriever=retriever, max_generation_len=164,min_prob=0.3)
            response = flare.run(prompt)
            st.write(response)
            st.write(cb)
        except Exception as e:
            st.warning(e)
            st.write("That was a difficult question!  I could choked on it!!  Can you please try again with rephrasing it a bit?")
            st.write(cb)
            print(e)