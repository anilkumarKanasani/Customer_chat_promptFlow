from dotenv import load_dotenv
load_dotenv()

import os

from promptflow.tools.common import init_openai_client
from promptflow.connections import OpenAIConnection
from promptflow.core import tool

@tool
def get_embedding(question: str):
    connection = OpenAIConnection(
                    api_key=os.environ["OPENAI_API_KEY"],
                    name="school_ep_openai_connection"
                    )
                
    client = init_openai_client(connection)

    return client.embeddings.create(
            input=question,
            model=os.environ["OPENAI_EMBD_MODEL"]
        ).data[0].embedding