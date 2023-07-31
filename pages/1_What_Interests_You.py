import streamlit as st
from st_pages import Page, Section, add_page_title, show_pages, hide_pages
from st_pages import add_indentation

add_page_title(":key: Which API would you like to use?", also_indent=True)  # Optional method to add title and icon to current page
# Also calls add_indentation() by default, which indents pages within a section

def aoai():
    show_pages(
        [
            Page("pages/0_Home.py", "Home", "🏠"),
            Section(name="Data Indexing Ops", icon=":notebook_with_decorative_cover:"),
            Page("pages/2_Upload_Documents.py", "Upload Documents", ":zap:"),
            Page("pages/30_Clean_Up_Chroma_and_FAISS.py", "Clean  up Indexes", ":collision:"),
            Page("pages/3_Index_PDFnTXT_Into_ChromaDB_Store.py", "Index to Chroma & FAISS", ":pencil:"),
            Section(name="Data Checking Ops", icon=":books:"),
            Page("pages/20_Query_ChromaDB.py", "Query Chroma Datastore", ":green_book:"),
            Page("pages/25_Query_FAISS.py", "Query FAISS Indexes", ":orange_book:"),
            Page("pages/40_EmbeddingsSearch_Chroma_and_FAISS.py", "Embedding Search - Chroma & FAISS", ":blue_book:"),
            Section(name="Azure OpenAI Searches", icon=":bulb:"),
            Page("pages/200_Q&A_with_Azure_Open_AI.py", "Q&A with Azure OpenAI", ":mag:"),
            Page("pages/210_Q&A_with_AOI_ACS_Kusto.py", "Q&A with AOAI ACS Kusto", ":mag:"),
            Page("pages/230_Talk_with_Azure_Open_AI.py", "ChatGPT Agent - Azure OpenAI", ":robot_face:"),
            Page("pages/240_Find_From_Website_AOAI.py", "Search Web and Open AI it!", ":earth_americas:"),
            Page("pages/5000_Feedback.py", "Feedback", ":mailbox_with_mail:", in_section=False),
        ]
    )
    add_indentation()

def aoi():
    show_pages(
        [
            Page("pages/0_Home.py", "Home", "🏠"),
            Section(name="Data Indexing Ops", icon=":notebook_with_decorative_cover:"),
            Page("pages/2_Upload_Documents.py", "Upload Documents", ":zap:"),
            Page("pages/30_Clean_Up_Chroma_and_FAISS.py", "Clean  up Indexes", ":collision:"),
            Page("pages/3_Index_PDFnTXT_Into_ChromaDB_Store.py", "Index to Chroma & FAISS", ":pencil:"),
            Section(name="Data Checking Ops", icon=":books:"),
            Page("pages/20_Query_ChromaDB.py", "Query Chroma Datastore", ":green_book:"),
            Page("pages/25_Query_FAISS.py", "Query FAISS Indexes", ":orange_book:"),
            Page("pages/40_EmbeddingsSearch_Chroma_and_FAISS.py", "Embedding Search - Chroma & FAISS", ":blue_book:"),
            Section(name="OpenAI Searches", icon=":bulb:"),
            Page("pages/100_Q&A_with_Open_AI.py", "Q&A with OpenAI", ":mag:"),
            Page("pages/130_Talk_with_Open_AI.py", "ChatGPT Agent - OpenAI", ":robot_face:"),
            Page("pages/140_Find_From_Website_AOI.py", "Search Web and Open AI it!", ":earth_americas:"),
            Page("pages/150_FLARE_AOI.py", "Search with Forward-Looking Active RAG (FLARE)", ":earth_americas:"),
            Page("pages/160_Self_Ask_AOI.py", "Search with Self-Ask prompting", ":earth_americas:"),
            Page("pages/5000_Feedback.py", "Feedback", ":mailbox_with_mail:", in_section=False),
        ]
    )
    add_indentation()

col1, col2 = st.columns(2, gap="large")

with col1:
    st.header("Azure OpenAI")
    
with col2:
    st.header("OpenAI")
   
st.write()

col1, col2 = st.columns(2, gap="large")

with col1:
    st.info('Have you setup Azure OpenAI variables (base url, version and key) in .env file?  If yes, go ahead and click the button below to start using OpenAI.', icon="ℹ️")

with col2:
    st.info('Have you setup OpenAI key in .env file?  If yes, go ahead and click the button below to start using OpenAI.', icon="ℹ️")

col1, col2 = st.columns(2, gap="large")

with col1:
    placeholder = st.empty()
    btn = placeholder.button('Run Samples using **Azure OpenAI**', disabled=False, key='1', use_container_width=True, type="primary")
    if btn:
        aoai()
        st.success("You have chosen to use **Azure OpenAI**", icon="✅")
        st.success("Your choice has been recorded. Please use the items in the left navigation bar to proceed with your exploration.  This page will no more be available.  If you wish to choose a differnt API, you will need to restart the application, due to shared variables across the two APIs on LangChain.  Once that issue is fixed, you will be able to change the APIs without having to restart.")

with col2:
    placeholder2 = st.empty()
    btn2 = placeholder2.button('Run Samples using **OpenAI**', disabled=False, key='11', use_container_width=True, type="primary")
    if btn2:
        aoi()
        st.success("You have chosen to use **OpenAI**", icon="✅")
        st.success("Your choice has been recorded. Please use the items in the left navigation bar to proceed with your exploration.  This page will no more be available.  If you wish to choose a differnt API, you will need to restart the application, due to shared variables across the two APIs on LangChain.  Once that issue is fixed, you will be able to change the APIs without having to restart.")

if btn or btn2:
    placeholder2.button('Run Samples using **OpenAI**', disabled=True, key='22', use_container_width=True, type="secondary")
    placeholder.button('Run Samples using **Azure OpenAI**', disabled=True, key='2', use_container_width=True, type="secondary")

add_indentation()       