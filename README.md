# 🦜🤗  Search with LangChain, HuggingFace embeddings and OpenAI

This project will help you learn the basics to -
- Index multiple documents in a repository using HuggingFace embeddings. 
- Save them in Chroma for recall. 
- Create a webpage to prompt for user input, query the Chroma database and ask OpenAI LLM for response. 
- Bonus: Get details on cost of the call (AI tokens and cost) and also get similar information document search on the store.

Link to the video recording - https://youtu.be/qTZMUaFU1Sc

# Setup the sample
To use the script, you will need to follow these steps:
- Clone the repository via `git clone https://github.com/ushakrishnan/SearchWithOpenAI.git` and `cd` into the cloned repository.
- Install the required packages: `pip install -r requirements.txt`
- Copy the .env.template file to .env: `cp .env.template .env`. This is where you will set the following variables.
- Set your OpenAI API key in the OPENAI_API_KEY
   
# Run the sample
- Rebuild index (feel free to add more PDFs ONLY into the directory `sou` for them to be added to the index)
  - If you would like to clean up your db from earlier runs - `rm -r db`
  - Setup Chroma store and load embeddings / index into store: `python3 loaddocs.py`
- Run the script: `streamlit run app.py`

# What to expect
Streamlit will spin up a page that will look like this
<img src=/assets/start.png>
Now go ahead, and ask you questions about the two "State of the Union" speech pdfs you had indexed (some ideas - when were the speeches made? What were the dates that the speeches were made? Summarize both speeches in 100 words or less. What did the president say about affordable care act?)
<img src=/assets/page.png height=400>

# Packages used
- Streamlit - https://github.com/streamlit/streamlit
- LangChain - https://github.com/hwchase17/langchain
- OpenAI - https://github.com/openai/openai-python
- Chroma - https://github.com/chroma-core/chroma
- TikToken - https://github.com/openai/tiktoken

Have fun creating making your own searchable library of PDFs.