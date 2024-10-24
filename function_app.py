import azure.functions as func
import logging
import os
import openai
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential

app = func.FunctionApp()


# Initializes Azure OpenAI environment
def init():
    global credential
    global AZURE_OPENAI_ENDPOINT
    global AZURE_OPENAI_KEY
    global AZURE_OPENAI_CHATGPT_DEPLOYMENT
    global OPENAI_API_VERSION

    # Use the Entra Id DefaultAzureCredential to get the token
    credential = DefaultAzureCredential()
    # Set the API type to `azure_ad`
    os.environ["OPENAI_API_TYPE"] = "azure_ad"
    # Set the API_KEY to the token from the Azure credential
    os.environ["OPENAI_API_KEY"] = credential.get_token(
        "https://cognitiveservices.azure.com/.default"
        ).token

    # Initialize Azure OpenAI environment
    AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_KEY = credential.get_token(
        "https://cognitiveservices.azure.com/.default"
        ).token
    AZURE_OPENAI_CHATGPT_DEPLOYMENT = os.environ.get(
        "AZURE_OPENAI_CHATGPT_DEPLOYMENT") or "chat"
    OPENAI_API_VERSION = os.environ.get(
        "OPENAI_API_VERSION") or "2023-05-15"

    # Configure base OpenAI framework for LangChain and/or llm
    openai.api_key = AZURE_OPENAI_KEY
    openai.api_base = AZURE_OPENAI_ENDPOINT
    openai.api_type = "azure"
    openai.api_version = OPENAI_API_VERSION


# Initialize Azure OpenAI environment
init()


# Function App entry point route for /api/ask
@app.function_name(name="ask")
@app.route(route="ask", auth_level="function", methods=["POST"])
def main(req):

    try:
        req_body = req.get_json()
        prompt = req_body.get("prompt")
    except ValueError:
        raise RuntimeError("prompt data must be set in POST.")
    else:
        if not prompt:
            raise RuntimeError("prompt data must be set in POST.")

    # LangChain user code goes here
    llm = AzureChatOpenAI(
        deployment_name=AZURE_OPENAI_CHATGPT_DEPLOYMENT,
        temperature=0.3
        )
    llm_prompt = PromptTemplate.from_template(
        "The following is a conversation with an AI assistant. " +
        "The assistant is helpful.\n\n" +
        "A:How can I help you today?\n" +
        "Human: {human_prompt}?"
        )
    formatted_prompt = llm_prompt.format(human_prompt=prompt)

    response = llm.invoke(formatted_prompt)
    logging.info(response.content)

    return func.HttpResponse(response.content)
