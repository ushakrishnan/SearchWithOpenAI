import streamlit as st
from pathlib import Path

from st_pages import Page, Section, add_page_title, show_pages, hide_pages
from st_pages import add_indentation

add_page_title("🏠 Home", also_indent=True)  # Optional method to add title and icon to current page
# Also calls add_indentation() by default, which indents pages within a section
add_indentation() 

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text(encoding='utf-8', errors='ignore')

intro_markdown = read_markdown_file("pages/home.md")
st.markdown(intro_markdown, unsafe_allow_html=True)