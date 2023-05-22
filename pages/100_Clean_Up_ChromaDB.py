# Bring in streamlit for UI/app interface
import streamlit as st
from common.funs import deletestore

st.title("🦜🔗🤗 This will delete all indexed information")

def start_capture():
    #delete documents and store
    result = deletestore(collection_name="sou_coll",persist_directory="db/")
    print(result)
    st.write("Get a Clean Start.  All indexes have been cleared.")

if st.button("⚠️ Delete Store and All Docs - Irreversible Action"):
    st.write(start_capture())