from typing import List
import os
from promptflow.core import tool
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import (
    VectorizedQuery,
)

@tool
def retrieve_documentation(
    question: str,
    embedding: List[float],
    index_name:str = "product-info-index",
) -> str:

    
    search_client = SearchClient(
        endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
        index_name=index_name,
        credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"])
    )

    vector_query = VectorizedQuery(
        vector=embedding, k_nearest_neighbors=3, fields="contentVector"
    )

    results = search_client.search(
        search_text=question,
        vector_queries=[vector_query],
        query_type="simple",
        top=3,
    )

    docs = [
        {
            "id": doc["id"],
            "title": doc["title"],
            "content": doc["content"],
            "url": doc["url"],
        }
        for doc in results
    ]

    return docs