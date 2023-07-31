import re
import os

import numpy as np

from langchain.schema import BaseRetriever
from langchain.callbacks.manager import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
)
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import Document
from typing import Any, List
from langchain.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
# Load default environment variables (.env)
load_dotenv()
serper_api_key = os.environ["SERPAPI_API_KEY"]

class SerperSearchRetriever(BaseRetriever):
    search: GoogleSerperAPIWrapper = None

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun, **kwargs: Any
    ) -> List[Document]:
        return [Document(page_content=self.search.run(query))]

    async def _aget_relevant_documents(
        self,
        query: str,
        *,
        run_manager: AsyncCallbackManagerForRetrieverRun,
        **kwargs: Any,
    ) -> List[Document]:
        raise NotImplementedError()


retriever = SerperSearchRetriever(search=GoogleSerperAPIWrapper(serper_api_key=serper_api_key))