from dotenv import load_dotenv
load_dotenv()

import os
from promptflow.core import tool
from azure.cosmos import CosmosClient
from azure.core.credentials import AzureKeyCredential


@tool
def get_customer(customerId: str) -> str:
    try:
        url = os.environ["COSMOS_ENDPOINT"]
        client = CosmosClient(url=url, credential=AzureKeyCredential(os.environ["COSMOS_KEY"]))
        db = client.get_database_client("contoso-outdoor")
        container = db.get_container_client("customers")
        response = container.read_item(item=str(customerId), partition_key=str(customerId))
        response["orders"] = response["orders"][:2]
        return response
    except Exception as e:
        print(f"Error retrieving customer: {e}")
        return None