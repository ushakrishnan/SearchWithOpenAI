import streamlit as st
from pathlib import Path

def read_markdown_file(md_file):
    return Path(md_file).read_text(encoding='utf-8', errors='ignore')

intro_markdown = read_markdown_file("README.md")
st.markdown(intro_markdown, unsafe_allow_html=True)