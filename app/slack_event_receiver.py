from fastapi import FastAPI  
import json, os
import openai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import threading
import app.custom_functions as cf
from dotenv import load_dotenv
import sentry_sdk
from . import schemas 

load_dotenv()

GPT_API_KEY = os.getenv("GPT_API_KEY")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SENTRY_DSN = os.getenv("SENTRY_DSN")

def is_env_var_loaded(env_var_name):
    if env_var_name is not None:
        print(f"The environment variable {env_var_name} is loaded.")
    else:
        print(f"The environment variable {env_var_name} is not loaded.")

is_env_var_loaded(GPT_API_KEY)
is_env_var_loaded(SLACK_TOKEN)
is_env_var_loaded(SENTRY_DSN)

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

slack_client = WebClient(token=SLACK_TOKEN)
app = FastAPI()



def send_message_to_chatgpt(message):
    """
    - sends conversation buffer with message from user to openai and gets back the response 
    - if response have a function call, call that function and register the result in conversation buffer and send the conversation buffer back to openai. 
    - finally when no function call in the result, return the response.
    """

    global conversation_buffer
    openai.api_key=GPT_API_KEY
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message,
            functions=[
                {
                    "name": "create_ssh_user",
                    "description": "create ssh user in server",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "username": { "type": "string", "description": "username of user" },
                            "serverIP": {"type": "string", "description": "serverIP of server"},
                            "sshPubKey": {"type": "string", "description": "ssh public key of user"},
                        },
                        "required": ["username", "serverIP", "sshPubKey"],
                    },
                },
                {
                    "name": "get_namespaces",
                    "description": "get all namespaces name in a list format for the current cluster context",
                    "parameters": {"type": "object", "properties": {}, },
                },
                {
                    "name": "get_events",
                    "description": "get the events in a list format for the current cluster context",
                    "parameters": {"type": "object", "properties": {}, },
                },
                {
                    "name": "get_secrets",
                    "description": "get the secrets in a table format",
                    "parameters": {"type": "object", "properties": {}, },
                }
            ]
            )  
    print(response)

    message =  response.choices[0].message
    if 'function_call' in message:
        print("***********function call detected")
        available_functions = {
            "create_ssh_user": cf.create_ssh_user,
            "get_namespaces": cf.get_namespaces,
            "get_events": cf.get_events,
            "get_secrets": cf.get_secrets
        }  
        function_name=message['function_call']['name']
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(message["function_call"]["arguments"])
        if function_name == "create_ssh_user":
            function_response = fuction_to_call(
                username=function_args.get("username"),
                serverIP=function_args.get("serverIP"),
                sshPubKey=function_args.get("sshPubKey")
            )
        if function_name == "get_namespaces" or function_name == "get_events" or function_name == "get_secrets":
            function_response = fuction_to_call()

        conversation_buffer.append({"role": "function", "name": function_name, "content": function_response })
        gpt_function_response = send_message_to_chatgpt(conversation_buffer)
        return gpt_function_response
    print(conversation_buffer)
    return response

def send_response_to_slack(response, channel_id, event_ts ):
    """send response to slack returned from openai"""
    response = slack_client.chat_postMessage(
                    channel=channel_id,
                    text=response,
                    thread_ts = event_ts
                )
    print(response)
    return response

openai.api_key=GPT_API_KEY
conversation_buffer = []
conversation_buffer.append({"role": "system", "content": "you are a devops engineer"})

def handle_chat(event):
    """handle chat event from slack, interact with openai and send final response to slack"""
    global conversation_buffer
    if event.event.type and event.event.user == 'U05PQFAR942':
        if "goodbye" in event.event.text:
            print("***********clearing conversation buffer")
            conversation_buffer = []
            send_response_to_slack("Have a good day!", event.event.channel, event.event.event_ts  ) 
            return {"response": "Have a good day!"}
        else:
            user_message = event.event.text
            content = "user: " + user_message
            conversation_buffer.append({"role": "user",   "content" : content})
            print("***********sending conversation buffer to chatgpt: \n", conversation_buffer)
            gpt_response = send_message_to_chatgpt(conversation_buffer).choices[0].message
            if gpt_response.content:
                content = gpt_response.content
                conversation_buffer.append({"role": "assistant", "content": content})
                print("***********got a response from chatgpt, sending response to slack: \n", content)
                send_response_to_slack(content, event.event.channel, event.event.event_ts  ) 


@app.post("/api/slack/events")
async def receive_slack_event(event: schemas.SlackPayload):
    print("***********event received from slack: \n" , event)
    if event.type == "url_verification":
        return {"challenge": event.challenge}
    threading.Thread(target=handle_chat, args=(event,)).start()
    return {"challenge": event.challenge}            

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
