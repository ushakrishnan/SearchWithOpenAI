# Bring in streamlit for UI/app interface
import streamlit as st
from common.funs import getfromstore
from st_pages import add_indentation

st.title(":green_book: Documents Persisted in Chroma")
add_indentation()

#get document stores

def start_capture():
    store = getfromstore(collection_name="sou_coll")
    st.write(store.get())

if st.button("Fetch Details"):
    st.write(start_capture())