#!/usr/bin/env python3
from dotenv import load_dotenv

# Load default environment variables (.env)
load_dotenv()

# Import os to set API key
import os
# Import OpenAI as main LLM service
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

# Bring in streamlit for UI/app interface
import streamlit as st

# Import PDF document loaders...there's other ones as well!
from langchain.document_loaders import PyPDFLoader
# Import chroma as the vector store 
from langchain.vectorstores import Chroma

from common.funs import getfromstore

# Import vector store stuff
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo
)

# Create instance of OpenAI LLM
llm = OpenAI(temperature=0.1, verbose=True)

#get document store
store = getfromstore(collection_name="sou_coll")
#print(store.get(["metadatas"]))

# Create vectorstore info object - metadata repo?
vectorstore_info = VectorStoreInfo(
    name="sou",
    description="sou folder",
    vectorstore=store
)
# Convert the document store into a langchain toolkit
toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)

# Add the toolkit to an end-to-end LC
agent_executor = create_vectorstore_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

st.title("🦜🔗🤗 What would you like to know?")
st.write("This sample uses OpenAI")
# Create a text input box for the user
prompt = st.text_input('Input your prompt here:')

# If the user hits enter
if prompt:
    with get_openai_callback() as cb:
        try:
            # Then pass the prompt to the LLM
            response = agent_executor.run(prompt)
            # ...and write it out to the screen
            st.write(response)
            st.write(cb)
        except:
            st.warning
            st.write("That was a difficult question!  I could choked on it!!  Can you please try again with rephrasing it a bit?")
            st.write(cb)
    
    # Find the relevant pages
    search = store.similarity_search_with_score(prompt)
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
