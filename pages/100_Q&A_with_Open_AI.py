#!/usr/bin/env python3
# Import os to set API key
import os
# Bring in streamlit for UI/app interface
import streamlit as st
# Import OpenAI as main LLM service
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from common.funs import getfaissdata
# Import vector store stuff
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo
)
from st_pages import add_indentation
from dotenv import load_dotenv
# Load default environment variables (.env)
load_dotenv()

add_indentation()

openai_api_type = os.environ["OPENAI_API_TYPE"] ="open_ai"
openai_api_version = os.environ["OPENAI_API_VERSION"] = os.environ["OAI_OPENAI_API_VERSION"]
openai_api_base = os.environ["OPENAI_API_BASE"] = os.environ["OAI_OPENAI_API_BASE"]
openai_api_key = os.environ["OPENAI_API_KEY"] = os.environ["OAI_OPENAI_API_KEY"]

# Create instance of OpenAI LLM
llm = OpenAI(temperature=0.1, verbose=True, model="text-davinci-002", openai_api_base=openai_api_base, openai_api_key=openai_api_key )  # noqa: E501

#you can choose the index you would like to use by choosing from the two options below
#store = getfromstore(collection_name="sou_coll")
store = getfaissdata()
#print(store.get(["metadatas"]))

# Create vectorstore info object - metadata repo?
vectorstore_info = VectorStoreInfo(
    name="sou",
    description="sou folder",
    vectorstore=store
)
# Convert the document store into a langchain toolkit
toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info, llm=llm)

# Add the toolkit to an end-to-end LC
agent_executor = create_vectorstore_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    max_iterations=2, 
    early_stopping_method="generate"
)

st.title("🦜🔗🤗 What would you like to know?")
st.write("This sample uses **OpenAI**")
# Create a text input box for the user
prompt = st.text_input('Input your prompt here:')

# If the user hits enter
if len(prompt) > 0:
    print()
    with get_openai_callback() as cb:
        try:
            # Then pass the prompt to the LLM
            response = agent_executor.run(prompt)
            # ...and write it out to the screen
            st.write(response)
            st.write(cb)
        except Exception as e:
            st.warning(e)
            st.write("That was a difficult question!  I could choked on it!!  Can you please try again with rephrasing it a bit?")
            st.write(cb)
            print(e)
    
    # Find the relevant pages
    search = store.similarity_search_with_score(prompt, k=4)
    # Write out the first 
    try:
        st.write("This information was found in:")
        for doc in search:
            score = doc[1]
            try:
                page_num = doc[0].metadata['page']
            except:
                page_num = "txt snippets"
            source = doc[0].metadata['source']
            # With a streamlit expander  
            with st.expander("Source: " + str(source) + " - Page: " + str(page_num) + "; Similarity Score: " + str(score) ):
                st.write(doc[0].page_content)
    except:
        print("unable to get source document detail")