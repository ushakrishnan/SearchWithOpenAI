# Bring in streamlit for UI/app interface
import streamlit as st
from common.funs import deletestore

st.title("🦜🔗🤗 This will delete all indexed information")

def start_capture():
    #delete documents and store
    result = deletestore(collection_name="sou_coll",persist_directory="db/")
    print(result)
    st.write("Get a Clean Start.  All indexes have been cleared.")
    st.write("This command should have deleted all files in your 'db' folder in your file structure.  In some operating systems and security settings, the folder is not fully  cleaned up.  Please check to make sure your db folder does not contain any files or folders, if you want to start with clean store.")

if st.button("⚠️ Delete Store and All Docs - Irreversible Action"):
    st.write(start_capture())