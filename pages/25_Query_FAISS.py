# Bring in streamlit for UI/app interface
import streamlit as st
from common.funs import getfaissdata
from langchain.vectorstores import FAISS
from st_pages import add_indentation

st.title(":orange_book:  Documents Persisted in FAISS")
add_indentation()

def start_capture():
    store = getfaissdata()
    st.write(store.index_to_docstore_id.items())

if st.button("Fetch Details"):
    st.write(start_capture())