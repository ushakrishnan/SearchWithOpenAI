import chromadb
import os
from chromadb.config import Settings
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings 
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFDirectoryLoader, DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter


def loadstore(val):
    return("hello " + val)



def getfromstore(collection_name="tdocsfolder"):
    # Equivalent to SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #embeddings = SentenceTransformerEmbeddings('all-MiniLM-L6-v2')
    #chroma uses by default
    #sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    store = Chroma(collection_name=collection_name, embedding_function=embeddings, persist_directory="db/")
    return(store)



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
        return(store)
    else:
        return()

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
    except:
        print("Have the files been cleanedup already?")
    return val