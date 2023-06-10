import chromadb
import os
from chromadb.config import Settings
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings 
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFDirectoryLoader, DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.retrievers import AzureCognitiveSearchRetriever
import streamlit as st
#!/usr/bin/env python3
from dotenv import load_dotenv
# Load default environment variables (.env)
load_dotenv()

def getfromacs():
    service_name = os.environ["AZURE_COGNITIVE_SEARCH_SERVICE_NAME"]
    index_name = os.environ["AZURE_COGNITIVE_SEARCH_INDEX_NAME"]
    api_key = os.environ["AZURE_COGNITIVE_SEARCH_API_KEY"]
    retriever = AzureCognitiveSearchRetriever(content_key="content", service_name=service_name, index_name=index_name, api_key=api_key)
    docs = retriever.get_relevant_documents("*")
    if len(docs) > 0:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        fstore = FAISS.from_documents(docs,embedding=embeddings)
        fstore.save_local("./faiss/faiss_acs")
        return(fstore)
    else:
        return()

def getfromstore(collection_name="tdocsfolder"):
    # Equivalent to SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #embeddings = SentenceTransformerEmbeddings('all-MiniLM-L6-v2')
    #chroma uses by default
    #sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    store = Chroma(collection_name=collection_name, embedding_function=embeddings, persist_directory="db/")
    return(store)

def getfaissdata():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    storepdf = FAISS.load_local("./faiss/faiss_indexpdf", embeddings)
    storetxt = FAISS.load_local("./faiss/faiss_indextxt", embeddings)
    storepdf.merge_from(storetxt)
    return storepdf

def addtostorepdf(folder_name, collection_name='db', persist_directory="db/"):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    loader = PyPDFDirectoryLoader(folder_name + "/")
    # Split pages from pdf (use load and split for pages, use load to use document chunks)
    #pages = loader.load_and_split()
    pages = loader.load()
    print("Number of PDF pages to be indexed: " + str(len(pages)))
    if len(pages) > 0:
        #----two additional to break into smaller chunks start-----
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"])
        docs = text_splitter.split_documents(pages)
        #----two additional to break into smaller chunks end-----
        # Load documents into vector database aka ChromaDB
        store = Chroma.from_documents(docs, embedding=embeddings, collection_name=collection_name, persist_directory=persist_directory)
        store.persist()
        fstore = FAISS.from_documents(docs,embedding=embeddings)
        fstore.save_local("./faiss/faiss_indexpdf")
        return(store)
    else:
        return()

def addtostoretxt(folder_name, collection_name='db', persist_directory="db/"):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    loader = DirectoryLoader(folder_name + "/", glob="**/*.txt",loader_cls=TextLoader, silent_errors=True)
    pages = loader.load()
    print("Number of TXT documents to be indexed: " + str(len(pages)))
    if len(pages) > 0:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        docs = text_splitter.split_documents(pages)
        store = Chroma.from_documents(docs, embedding=embeddings, collection_name=collection_name, persist_directory=persist_directory)
        store.persist()
        fstore = FAISS.from_documents(docs,embedding=embeddings)
        fstore.save_local("./faiss/faiss_indextxt")
        return(store)
    else:
        return()

def addtochattxt(prompt, collection_name='chat', persist_directory="chat/"):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_text(prompt)
    store = Chroma.from_texts(docs, embedding=embeddings, collection_name=collection_name, persist_directory=persist_directory)
    store.persist()
    return(store)

def getchatstore(collection_name="chat"):
    # Equivalent to SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #embeddings = SentenceTransformerEmbeddings('all-MiniLM-L6-v2')
    #chroma uses by default
    #sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    store = Chroma(collection_name=collection_name, embedding_function=embeddings, persist_directory="chat/")
    return(store)

def deletestore(collection_name='db', persist_directory="db/"):
    client = chromadb.Client(Settings(persist_directory=persist_directory))
    try:
        client.delete_collection(collection_name)
    except:
        print("Has the collection been already deleted?")
    val = client.reset()
    try:
        os.rmdir("db/index")  
        os.remove("db/chroma-collections.parquet")  
        os.remove("db/chroma-embeddings.parquet")
        os.rmdir("faiss/faiss_indexpdf")  
        os.rmdir("faiss/faiss_indextxt")  
    except:
        print("Have the files been cleanedup already?")
    return val

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):
        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
    return conversation_string