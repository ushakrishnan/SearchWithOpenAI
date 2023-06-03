# Bring in streamlit for UI/app interface
import streamlit as st
import os
from st_pages import add_indentation

st.title(":zap: Upload Documents for Indexing")
add_indentation()

uploaded_files = st.file_uploader("Select PDF or TXT files to upload", accept_multiple_files=True,type=["txt","PDF"],)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    #st.write(bytes_data)
    with open(os.path.join("sou",uploaded_file.name),"wb") as f: 
        f.write(uploaded_file.getbuffer())         
        st.success("Saved File")