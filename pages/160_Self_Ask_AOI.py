# Import os to set API key
import os
# Import OpenAI as main LLM service
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.llms.openai import OpenAI
from langchain.agents import initialize_agent, AgentType, Tool

from common.webcatcher import searchweb
# Bring in streamlit for UI/app interface
import streamlit as st

from st_pages import add_indentation

#!/usr/bin/env python3
from dotenv import load_dotenv
# Load default environment variables (.env)
load_dotenv()

add_indentation()

openai_api_type = os.environ["OPENAI_API_TYPE"] ="open_ai"
openai_api_version = os.environ["OPENAI_API_VERSION"] = os.environ["OAI_OPENAI_API_VERSION"]
openai_api_base = os.environ["OPENAI_API_BASE"] = os.environ["OAI_OPENAI_API_BASE"]
openai_api_key = os.environ["OPENAI_API_KEY"] = os.environ["OAI_OPENAI_API_KEY"]
serper_api_key = os.environ["SERPER_API_KEY"]

print(serper_api_key)

# Create instance of OpenAI LLM
llm = OpenAI(temperature=0.1, verbose=True, model="text-davinci-002", openai_api_base=openai_api_base,  openai_api_key=openai_api_key )
search = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)

st.title("🦜🔗🤗 What would you like to know?")
st.write("This sample uses **OpenAI and Serper**")
# Create a text input box for the user
prompt = st.text_input('Input your prompt here: ex. what are the ingredients for fortify alchemy potion')

# If the user hits enter
if len(prompt) > 0:
    with get_openai_callback() as cb:
        try:
            # tools = load_tools(["google-serper"], llm=llm)
            # tools = load_tools(["serpapi"], llm=llm)
            # tools = load_tools(["google-search"], llm=llm )
            tools = [
                Tool(
                    name="Intermediate Answer",
                    func=search.run,
                    description="useful for when you need to ask with search",
                )
            ]
            agent_executor = initialize_agent(
                tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True
            )
            agent_executor.run(prompt)
            response = agent_executor.run(prompt)
            # ...and write it out to the screen
            st.write(response)
            st.write(cb)
        except Exception as e:
            st.warning(str.replace(str(e), "Could not parse output:",""))
            # st.write("That was a difficult question!  I choked on it!!  Can you please try again with rephrasing it a bit?")
            st.write(cb)
            print(e)