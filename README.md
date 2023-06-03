# Azure Functions
## LangChain with Azure OpenAI and ChatGPT (Python v2 Function)

This sample shows how to take a human prompt as HTTP Get or Post input, calculates the completions using chains of human input and templates.  This is a starting point that can be used for more sophisticated chains.  

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=575770869)

## Run on your local environment

### Pre-reqs
1) [Python 3.8+](https://www.python.org/) 
2) [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cmacos%2Ccsharp%2Cportal%2Cbash#install-the-azure-functions-core-tools)
3) [Azure OpenAPI API key, endpoint, and deployment](https://portal.azure.com) 
4) Add this `local.settings.json` file to this folder to simplify local development and include Key from step 3

`./local.settings.json`
```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "AZURE_OPENAI_KEY": "...",
    "AZURE_OPENAI_ENDPOINT": "https://<service_name>.openai.azure.com/",
    "AZURE_OPENAI_SERVICE": "...",
    "AZURE_OPENAI_CHATGPT_DEPLOYMENT": "...",
    "USE_LANGCHAIN": "True"
  }
}
```

### Using Functions CLI
1) Open a new terminal and do the following:

```bash
pip3 install -r requirements.text
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


## Source Code

The key code that makes this work is as follows in [function_app.py](./function_app.py).  You can customize this or learn more snippets using the [LangChain Quickstart Guide](https://python.langchain.com/en/latest/getting_started/getting_started.html).

```python
llm = AzureOpenAI(deployment_name=AZURE_OPENAI_CHATGPT_DEPLOYMENT, temperature=0.3, openai_api_key=AZURE_OPENAI_KEY)

llm_prompt = PromptTemplate(
    input_variables=["human_prompt"],
    template="The following is a conversation with an AI assistant. The assistant is helpful.\n\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: {human_prompt}?",
)

from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=llm_prompt)

return chain.run(prompt) # prompt is human input from request body
```

## Deploy to Azure

The easiest way to deploy this app is using the [Azure Dev CLI aka AZD](https://aka.ms/azd).  If you open this repo in GitHub CodeSpaces the AZD tooling is already preinstalled.

To provision and deploy:
```bash
azd up
```
