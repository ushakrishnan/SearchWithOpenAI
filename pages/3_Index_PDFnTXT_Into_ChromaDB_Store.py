# Bring in streamlit for UI/app interface
import streamlit as st
from common.funs import addtostorepdf, addtostoretxt, getfromstore

st.title("🦜🔗🤗 Index content and metadata into ChromaDB Store")

def start_capture():
    #load documents into store
    store2 = addtostorepdf(folder_name="sou",collection_name="sou_coll",persist_directory="db/")
    print(store2.get(["metadatas"]))

    store2 = addtostoretxt(folder_name="sou",collection_name="sou_coll",persist_directory="db/")
    print(store2.get(["metadatas"]))

    #get document store
    store = getfromstore(collection_name="sou_coll")
    st.write(store.get(["metadatas"]))

if st.button("💡 Index documents in folder to ChromaDB"):
    st.write(start_capture())