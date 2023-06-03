#!/usr/bin/env python3
from dotenv import load_dotenv

# Load default environment variables (.env)
load_dotenv()

# Import os to set API key
import os
# Import OpenAI as main LLM service
from langchain.llms import OpenAI

# Bring in streamlit for UI/app interface
import streamlit as st

# Import PDF document loaders...there's other ones as well!
from langchain.document_loaders import PyPDFLoader

from common.funs import getfromstore, getfaissdata
from st_pages import add_indentation

add_indentation()

st.title(":blue_book: What would you like to know?")
# Create a text input box for the user
prompt = st.text_input('Input your prompt here:')

if len(prompt) > 0:
    #get document store
    store = getfromstore(collection_name="sou_coll")
    # Find the relevant pages
    search = store.similarity_search_with_score(prompt,k=2)
    # Write out the first 
    try:
        st.write("Store - Similarity Search with Score:")
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

    #get FAISS index
    fstore = getfaissdata()
    # Find the relevant pages
    fsearch = fstore.similarity_search_with_score(prompt, k=2)
    # Write out the first 
    try:
        st.write("FAISS - Similarity Search:")
        for doc in fsearch:
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
else:
    st.write("Why don't you add your question in the textbox and press enter to test me?")