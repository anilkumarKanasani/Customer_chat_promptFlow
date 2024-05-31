from dotenv import load_dotenv
load_dotenv()

import os
from promptflow.core import tool
from azure.cosmos import CosmosClient
from azure.core.credentials import AzureKeyCredential


@tool
def get_product(productId: str) -> str:
    try:
        url = os.environ["COSMOS_ENDPOINT"]
        client = CosmosClient(url=url, credential=AzureKeyCredential(os.environ["COSMOS_KEY"]))
        db = client.get_database_client("contoso-outdoor")
        container = db.get_container_client("products")
        response = container.read_item(item=str(productId), partition_key=str(productId))
        return response
    except Exception as e:
        print(f"Error retrieving product: {e}")
        return None