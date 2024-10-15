---
page_type: sample
languages:
- azdeveloper
- python
- bicep
products:
- azure
- azure-functions
- azure-openai
urlFragment: function-python-ai-langchain
name: Azure Functions - LangChain with Azure OpenAI and ChatGPT (Python v2 Function)
description: Using human prompt with Python as HTTP Get or Post input, calculates the completions using chains of human input and templates. 
---
<!-- YAML front-matter schema: https://review.learn.microsoft.com/en-us/help/contribute/samples/process/onboarding?branch=main#supported-metadata-fields-for-readmemd -->

# Azure Functions
## LangChain with Azure OpenAI and ChatGPT (Python v2 Function)

This sample shows how to take a human prompt as HTTP Get or Post input, calculates the completions using chains of human input and templates.  This is a starting point that can be used for more sophisticated chains.  

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=575770869)

## Run on your local environment

### Pre-reqs
1) [Python 3.8+](https://www.python.org/) 
2) [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cmacos%2Ccsharp%2Cportal%2Cbash#install-the-azure-functions-core-tools)
3) [Azure Developer CLI](https://aka.ms/azd)
4) Once you have your Azure subscription, run the following in a new terminal window to create Azure OpenAI and other resources needed:
```bash
azd provision
```

Take note of the value of `AZURE_OPENAI_ENDPOINT` which can be found in `./.azure/<env name from azd provision>/.env`.  It will look something like:
```bash
AZURE_OPENAI_ENDPOINT="https://cog-<unique string>.openai.azure.com/"
```

5) Add this `local.settings.json` file to the root of the repo folder to simplify local development.  Replace `AZURE_OPENAI_ENDPOINT` with your value from step 4.  Optionally you can choose a different model deployment in `AZURE_OPENAI_CHATGPT_DEPLOYMENT`.  This file will be gitignored to protect secrets from committing to your repo, however by default the sample uses Entra identity (user identity and mananaged identity) so it is secretless.  
```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "AZURE_OPENAI_ENDPOINT": "https://<your deployment>.openai.azure.com/",
    "AZURE_OPENAI_CHATGPT_DEPLOYMENT": "chat",
    "OPENAI_API_VERSION": "2023-05-15"
  }
}
```

### Using Functions CLI
1) Open a new terminal and do the following:

```bash
pip3 install -r requirements.txt
func start
```
2) Using your favorite REST client, e.g. [RestClient in VS Code](https://marketplace.visualstudio.com/items?itemName=humao.rest-client), PostMan, curl, make a post.  `test.http` has been provided to run this quickly.   

Terminal:
```bash
curl -i -X POST http://localhost:7071/api/ask/ \
  -H "Content-Type: text/json" \
  --data-binary "@testdata.json"
```

`testdata.json`
```json
{
    "prompt": "What is a good feature of Azure Functions?"
}
```

`test.http`
```bash

POST http://localhost:7071/api/ask HTTP/1.1
content-type: application/json

{
    "prompt": "What is a good feature of Azure Functions?"
}
```

### Using Visual Studio Code
1) Open this repo in VS Code:
```bash
code .
```

2) Follow the prompts to load Function.  It is recommended to Initialize the Functions Project for VS Code, and also to enable a virtual environment for your chosen version of Python.  

3) Run and Debug `F5` the app

4) Test using same REST client steps above

## Deploy to Azure

The easiest way to deploy this app is using the [Azure Dev CLI](https://aka.ms/azd).  If you open this repo in GitHub CodeSpaces the AZD tooling is already preinstalled.

To provision and deploy:
```bash
azd up
```

## Source Code

The key code that makes the prompting and completion work is as follows in [function_app.py](function_app.py).  The `/api/ask` function and route expects a prompt to come in the POST body using a standard HTTP Trigger in Python.  Then once the environment variables are set to configure OpenAI and LangChain frameworks via `init()` function, we can leverage favorite aspects of LangChain in the `main()` (ask) function.  In this simple example we take a prompt, build a better prompt from a template, and then invoke the LLM.  By default the LLM deployment is `gpt-35-turbo` as defined in [./infra/main.parameters.json](./infra/main.parameters.json) but you can experiment with other models and other aspects of Langchain's breadth of features.    

```python
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
```
