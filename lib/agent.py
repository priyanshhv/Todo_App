from lib.config import client
from lib.weather import create_task, get_tasks
import json

# description is the description of the function/parameter.
# It is what the model uses to understand the function
# description is the description of the function/parameter.
# It is what the model uses to understand the function
function_list = [
    {
        "name": "create_task",
        "description": "Create a new task",
        "parameters": {
            "type": "object",
            "properties": {
                "desc": {
                    "type": "string",
                    "description": "The description of the task",
                },
            },
            "required": ["desc"],
        },
    },
    {
        "name": "get_tasks",
        "description": "Get all tasks",
        "parameters": {},
    },
]


def agent(messages):
    # print(messages)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=function_list,
    ).choices[0]

    available_functions = {
        "create_task": create_task,
        "get_tasks": get_tasks,
    }

    finish_reason = response.finish_reason

    while finish_reason == "function_call":
        function_args = json.loads(response.message.function_call.arguments)
        function_to_call = available_functions[response.message.function_call.name]
        function_response = function_to_call(**function_args)  # function called here

        messages.append(
            {
                "role": "function",
                "name": response.message.function_call.name,
                "content": str(function_response),
            }
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=function_list,
        ).choices[0]

        finish_reason = response.finish_reason

    return response.message.content
