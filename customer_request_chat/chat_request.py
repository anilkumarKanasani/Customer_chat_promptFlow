from dotenv import load_dotenv
load_dotenv()

import os
import pathlib
from promptflow.connections import OpenAIConnection
from promptflow.core import (OpenAIModelConfiguration, Prompty, tool)


@tool
def get_response(customer, context, question, chat_history):
    connection = OpenAIConnection(
                    api_key=os.environ["OPENAI_API_KEY"],
                    name="school_ep_openai_connection"
                    )

    configuration = OpenAIModelConfiguration.from_connection(
            model=os.environ["OPENAI_MODEL"],
            connection=connection
        )
    override_model = {
        "configuration": configuration,
        "parameters": {"max_tokens": 512}
    }
    # get cwd
    data_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "./chat.prompty")
    prompty_obj = Prompty.load(data_path, model=override_model)

    result = prompty_obj(question = question, customer = customer, documentation = context)
    # print(result)
    return result

