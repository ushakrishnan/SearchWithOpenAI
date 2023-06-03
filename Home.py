import streamlit as st
from pathlib import Path
from st_pages import Page, Section, add_page_title, show_pages, hide_pages
from st_pages import add_indentation

show_pages(
    [
        Page("pages/0_Home.py", "Home", "🏠"),
        Page("pages/1_What_Interests_You.py", "Which API would you like to use?", ":key:"),
    ]
)

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text(encoding='utf-8', errors='ignore')

intro_markdown = read_markdown_file("README.md")
st.markdown(intro_markdown, unsafe_allow_html=True)