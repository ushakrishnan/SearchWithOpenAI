import chromadb
import os
import streamlit as st
import openai
import pandas as pd

from chromadb.config import Settings
from langchain.embeddings import HuggingFaceEmbeddings 
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFDirectoryLoader, DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.retrievers import AzureCognitiveSearchRetriever
from azure.kusto.data import KustoConnectionStringBuilder,KustoClient
from azure.kusto.ingest import QueuedIngestClient, IngestionProperties
from azure.kusto.data.data_format import DataFormat
from azure.kusto.data.helpers import dataframe_from_result_table

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
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"])  # noqa: E501
        docs = text_splitter.split_documents(pages)
        #----two additional to break into smaller chunks end-----
        # Load documents into vector database aka ChromaDB
        store = Chroma.from_documents(docs, embedding=embeddings, collection_name=collection_name, persist_directory=persist_directory)  # noqa: E501
        store.persist()
        fstore = FAISS.from_documents(docs,embedding=embeddings)
        fstore.save_local("./faiss/faiss_indexpdf")
        return(store)
    else:
        return()

def addtostoretxt(folder_name, collection_name='db', persist_directory="db/"):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    loader = DirectoryLoader(folder_name + "/", glob="**/*.txt",loader_cls=TextLoader, silent_errors=False)  # noqa: E501
    pages = loader.load()
    print("Number of TXT documents to be indexed: " + str(len(pages)))
    if len(pages) > 0:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        docs = text_splitter.split_documents(pages)
        store = Chroma.from_documents(docs, embedding=embeddings, collection_name=collection_name, persist_directory=persist_directory)  # noqa: E501
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
    store = Chroma.from_texts(docs, embedding=embeddings, collection_name=collection_name, persist_directory=persist_directory)  # noqa: E501
    store.persist()
    return(store)

def getchatstore(collection_name="chat"):
    # Equivalent to SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #embeddings = SentenceTransformerEmbeddings('all-MiniLM-L6-v2')
    #chroma uses by default
    #sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")  # noqa: E501
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

def add_docs_to_kusto():
        kusto_database = os.environ["KUSTO_DATABASE"]
        kusto_table_name = os.environ["KUSTO_TABLE_NAME"]  #We will be creating first then querying the same table
        kusto_cluster = os.environ["KUSTO_CLUSTER"]
        kusto_ingest_cluster = os.environ["KUSTO_INGEST_CLUSTER"]
        kusto_auth_app_id = os.environ["KUSTO_AUTH_APP_ID"]
        kusto_auth_app_key = os.environ["KUSTO_AUTH_APP_KEY"]
        kusto_auth_app_tenant_id = os.environ["KUSTO_AUTH_APP_TENANT_ID"]
        
        service_name = os.environ["AZURE_COGNITIVE_SEARCH_SERVICE_NAME"]
        index_name = os.environ["AZURE_COGNITIVE_SEARCH_INDEX_NAME"]
        api_key = os.environ["AZURE_COGNITIVE_SEARCH_API_KEY"]
        retriever = AzureCognitiveSearchRetriever(content_key="content", service_name=service_name, index_name=index_name, api_key=api_key)
        docs = retriever.get_relevant_documents("*")
        if len(docs) > 0:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
            docs = text_splitter.split_documents(docs)
            strs = []
            for doc in docs:
                if (len(doc.page_content) > 2):
                    strs.append(doc.page_content)
            print(strs)
            pd_df = embedlist(strs)
            connection_string = KustoConnectionStringBuilder.with_aad_application_key_authentication(kusto_cluster, kusto_auth_app_id, kusto_auth_app_key,kusto_auth_app_tenant_id)
            kusto_client = KustoClient(connection_string)
            kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(kusto_ingest_cluster, kusto_auth_app_id, kusto_auth_app_key,kusto_auth_app_tenant_id)
            ingestionclient = QueuedIngestClient(kcsb)

            ingestion_props = IngestionProperties(
            database=kusto_database,
            table=kusto_table_name,
            data_format=DataFormat.CSV,
            )
            if createtableadx(table_name=kusto_table_name, kusto_client=kusto_client, kusto_database=kusto_database):
                print(f"{kusto_table_name} Created.")
                #Once table is created write the content
                ingestionclient.ingest_from_dataframe(pd_df, ingestion_properties=ingestion_props)
            else:
                print(f"Failed to create table {kusto_table_name}.")
        else:
            return()


def embed(query):
    embedding_model = os.environ["AOAI_OPENAI_API_ENC_MODEL"]
    # Creates embedding vector from user query
    embedded_query = openai.Embedding.create(
            input=query,
            deployment_id=embedding_model, #replace with your deployment id
            chunk_size=1
    )["data"][0]["embedding"]
    return embedded_query

def createtableadx(table_name, kusto_client, kusto_database):
  try:
    create_table_command = f".create table {table_name} (Content: string, Embeddings: dynamic)"
    RESPONSE = kusto_client.execute_mgmt(kusto_database, create_table_command)
    print(f"{RESPONSE}")
    return True
  except:
    return False

def embedlist(content):
    resultList = []
    for page in content:
      Content = page
      Embeddings = embed(page)
      myList = [Content, Embeddings]
      resultList.append(myList)
    df = pd.DataFrame(resultList, columns=['Content', 'Embeddings'])
    return df

def getfromkusto(prompt):
    searchedEmbedding=prompt
    kusto_database = os.environ["KUSTO_DATABASE"]
    kusto_table_name = os.environ["KUSTO_TABLE_NAME"]  #We will be creating first then querying the same table
    kusto_cluster = os.environ["KUSTO_CLUSTER"]
    kusto_auth_app_id = os.environ["KUSTO_AUTH_APP_ID"]
    kusto_auth_app_key = os.environ["KUSTO_AUTH_APP_KEY"]
    kusto_auth_app_tenant_id = os.environ["KUSTO_AUTH_APP_TENANT_ID"]
    connection_string = KustoConnectionStringBuilder.with_aad_application_key_authentication(kusto_cluster, kusto_auth_app_id, kusto_auth_app_key,kusto_auth_app_tenant_id)
    kusto_client = KustoClient(connection_string)
    kusto_query = f"{kusto_table_name} | extend similarity = series_cosine_similarity_fl(dynamic('"+str(searchedEmbedding)+"'),Embeddings,1,1) | top 10 by similarity desc "
    # print(kusto_query)
    response = kusto_client.execute(kusto_database, kusto_query)
    df = dataframe_from_result_table(response.primary_results[0])
    content = "\n".join(df['Content'])
    return content

def experimentalchunktxt(value, collection_name='chat', persist_directory="chat/"):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10)
    docs = text_splitter.split_text(value)
    store = FAISS.from_texts(docs,embedding=embeddings)
    return(store)