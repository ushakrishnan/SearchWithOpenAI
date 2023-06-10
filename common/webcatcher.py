# Import os to set API key
import os
from langchain.utilities import BingSearchAPIWrapper
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

def searchweb(site = "", query=""):

    search = BingSearchAPIWrapper(k=2)
    metadata_result = search.results(query + ":" + site,3)

    urls = []
    raw_documents = []

    if len(metadata_result) == 0:
        print("Result : No good Bing Search Result was found")
    for result in metadata_result:
        urls.append(result["link"])

    loader = WebBaseLoader(urls)
    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    documents = text_splitter.split_documents(raw_documents)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    store = FAISS.from_documents(documents,embedding=embeddings)
    return store