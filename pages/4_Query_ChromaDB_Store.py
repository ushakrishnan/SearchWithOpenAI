# Bring in streamlit for UI/app interface
import streamlit as st
from common.funs import getfromstore

st.title("🦜🔗🤗  Documents Persisted in Vector Database")

#get document stores

def start_capture():
    store = getfromstore(collection_name="sou_coll")
    st.write(store.get())

if st.button("Fetch Details"):
    st.write(start_capture())