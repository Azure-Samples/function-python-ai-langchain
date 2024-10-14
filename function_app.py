import azure.functions as func
import logging
import os
import openai
from langchain.prompts import PromptTemplate
from langchain.llms.openai import AzureOpenAI

app = func.FunctionApp()


@app.function_name(name='ask')
@app.route(route='ask', auth_level='anonymous', methods=['POST'])
def main(req):

    prompt = req.params.get('prompt')
    if not prompt:
        try:
            req_body = req.get_json()
        except ValueError:
            raise RuntimeError("prompt data must be set in POST.")
        else: 
            prompt = req_body.get('prompt')
            if not prompt:
                raise RuntimeError("prompt data must be set in POST.")

    # init OpenAI: Replace these with your own values, either in env vars
    AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
    AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_CHATGPT_DEPLOYMENT = os.environ.get(
        "AZURE_OPENAI_CHATGPT_DEPLOYMENT") or "chat"
    if 'AZURE_OPENAI_KEY' not in os.environ:
        raise RuntimeError("No 'AZURE_OPENAI_KEY' env var set.")

    # configure azure openai for langchain and/or llm
    openai.api_key = AZURE_OPENAI_KEY
    openai.api_base = AZURE_OPENAI_ENDPOINT
    openai.api_type = 'azure'

    # this may change in the future
    # set this version in environment variables using OPENAI_API_VERSION
    openai.api_version = '2023-05-15'

    logging.info('Using Langchain')

    llm = AzureOpenAI(
        deployment_name=AZURE_OPENAI_CHATGPT_DEPLOYMENT,
        temperature=0.3,
        openai_api_key=AZURE_OPENAI_KEY
        )
    llm_prompt = PromptTemplate(
        input_variables=["human_prompt"],
        template="The following is a conversation with an AI assistant. " +
                 "The assistant is helpful.\n\n" +
                 "A:How can I help you today?\nHuman: {human_prompt}?",
    )
    from langchain.chains import LLMChain
    chain = LLMChain(llm=llm, prompt=llm_prompt)
    return chain.run(prompt)
