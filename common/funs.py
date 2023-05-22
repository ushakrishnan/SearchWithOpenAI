from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings 
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter


def loadstore(val):
    return("hello " + val)



def getfromstore(collection_name="tdocsfolder"):
    # Equivalent to SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #embeddings = SentenceTransformerEmbeddings('all-MiniLM-L6-v2')
    #chroma used by default
    #sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    store = Chroma(collection_name=collection_name, embedding_function=embeddings, persist_directory="db/")
    return(store)



def addtostore(folder_name, collection_name='db', persist_directory="db/"):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #embeddings = SentenceTransformerEmbeddings('all-MiniLM-L6-v2')
    loader = PyPDFDirectoryLoader(folder_name + "/")
    # Split pages from pdf (use load and split for pages, use load to use document chunks)
    #pages = loader.load_and_split()
    pages = loader.load()
    #----two additional to break into smaller chunks start-----
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"])
    #text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    docs = text_splitter.split_documents(pages)
    #----two additional to break into smaller chunks end-----
    # Load documents into vector database aka ChromaDB
    store = Chroma.from_documents(docs, embedding=embeddings, collection_name=collection_name, persist_directory=persist_directory)
    return(store)