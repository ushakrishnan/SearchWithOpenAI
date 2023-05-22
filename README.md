# 🦜🤗  Search with LangChain, HuggingFace embeddings and OpenAI

This project will help you learn the basics to -
- Index multiple documents in a repository using HuggingFace embeddings. 
- Provide directory / folder name where the pdf and txt files are and all pdf and txt files will be indexed.
- Save them in Chroma for recall. 
- Create a webpage to prompt for user input, query the Chroma database and ask OpenAI LLM for response. 
- Bonus: Get details on cost of the call (AI tokens and cost) and also get similar information document search on the store.

Link to the video recording - https://youtu.be/q27RbxcfGvE

# Setup the sample
To use the script, you will need to follow these steps:
- Clone the repository via `git clone https://github.com/ushakrishnan/SearchWithOpenAI.git` and `cd SearchWithOpenAI` into the cloned repository.
- Install the required packages: `pip install -r requirements.txt`
- Copy the .env.template file to .env: `cp .env.template .env`. This is where you will set the following variables.
- Set your OpenAI API key in the OPENAI_API_KEY and Azure OpenAI details in the env file
   
# Run the sample
- Run the script: `streamlit run Home.py`
- You will be able to from the web interface 
  - Clean up the Chroma vector database
  - Upload additional pdf / txt documents for adding to index / querying
  - Create fresh index and populate the vector store after clean up
  - Have a choice of using OpenAI or Azure OpenAI for doing your searches on the documents

# What to expect
Streamlit will spin up a page that will look like this
<img src="/assets/start.png" height=400>
Now go ahead, and ask you questions about the two "State of the Union" speech pdfs and txt you had indexed (some ideas - when were the speeches made? What were the dates that the speeches were made? Summarize both speeches in 100 words or less. What did the president say about affordable care act?)
<img src="/assets/page.png" height=400>

# Packages used
- Streamlit - https://github.com/streamlit/streamlit
- LangChain - https://github.com/hwchase17/langchain
- OpenAI - https://github.com/openai/openai-python
- Chroma - https://github.com/chroma-core/chroma
- TikToken - https://github.com/openai/tiktoken
- pypdf - https://github.com/py-pdf/pypdf
- Unstructured - https://github.com/Unstructured-IO/unstructured
- Cython - https://github.com/cython/cython

Have fun creating making your own searchable library of PDFs.