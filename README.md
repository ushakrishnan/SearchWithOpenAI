# 🦜🔗🤗  Search with LangChain, HuggingFace embeddings, Chroma, FAISS, Azure OpenAI and OpenAI

This project will help you learn the basics to -
- Index multiple documents in a repository using HuggingFace embeddings.
- Save the indexes in Chroma &  FAISS for recall.
- Cleanup / delete the indexes to start fresh.
- Query the FAISS and Chroma index / db.
- Search using embeddings (without having to sign up for any OpenAI) for similarity text snippets.
- Search with either OpenAI or Azure OpenAI.  You will use the "Which API would you like to use?" page to choose the API to use.
- Bonus: Get details on cost of the call (AI tokens and cost) and also get similar information document search on the store.

Link to the video recording - https://youtu.be/VaShd-0UoGg

# Features
1. Clean up indexes, add your documents to store (options: FAISS / Chroma / both)
2. Choose your OpenAI (options: OpenAI / Azure OpenAI) [See how](#choose-your-openai)
3. Q&A from the set of uploaded documents (options: FAISS / Chroma) [See how](#q-and-a-from-the-set-of-uploaded-documents)
4. Your own chatgpt (options: prompt engineer with your customized prompts) [See how](#your-own-chatgpt)
5. Search a specific website / whole web and feed to OpenAI for extracting informaiton (options: OpenAI / Azure OpenAI :: sample uses Bing Search) [See how](#search-web-for-information)

## Samples and Fetures:

### Choose your OpenAI
<img src="/assets/choice.gif" >
[Back to all features](# features)

### Q and A from the set of uploaded documents
Now go ahead, and ask you questions about the two "State of the Union" speech pdfs and txt you had indexed (some ideas - when were the speeches made? What were the dates that the speeches were made? Summarize both speeches in 100 words or less. What did the president say about affordable care act?)
<img src="/assets/qanda.gif"> 
[Back to all features](# features)

### Your own chatgpt
NEW Sample - Your own ChatGPT will be as below
<img src="/assets/chatgpt.gif">
[Back to all features](# features)

### Search web for information
New Sample - search your own website of the whole web.   Feed the results to ChatGPT for summarizing or answering questions.
<img src="/assets/searchweb.gif">
[Back to all features](# features)

# Setup the sample
To use the script, you will need to follow these steps:
- Clone the repository via `git clone https://github.com/ushakrishnan/SearchWithOpenAI.git` and `cd SearchWithOpenAI` into the cloned repository.
- Install the required packages: `pip install -r requirements.txt`
- Run `playwright install` to install playwright
- Copy the .env.template file to .env: `cp .env.template .env`. This is where you will set the following variables.
- Set your OpenAI API key in the OPENAI_API_KEY and Azure OpenAI details in the env file.  
   
## Run the sample
- Run the script: `streamlit run Home.py`

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


## Contributing

This repository is for educational purposes only. However, if you find an error in the code, feel free to open an issue or submit a pull request.


## Issues

If you encounter any issues or have suggestions for improvements, please open an issue in the GitHub repository. We appreciate your feedback and will do our best to address any problems.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to modify and distribute the code as per the terms of the license.