param name string
param location string = resourceGroup().location
param tags object = {}

param gptDeploymentName string = 'davinci'
param gptModelName string = 'text-davinci-003'
param gptDeploymentCapacity int = 30
param chatGptDeploymentName string = 'chat'
param chatGptModelName string = 'gpt-35-turbo'
param chatGptDeploymentCapacity int = 30

module openai '../core/ai/openai.bicep' = {
  name: 'ai-textanalytics'
  params: {
    name: name
    location: location
    tags: tags
    deployments: [
      {
        name: chatGptDeploymentName
        model: {
          format: 'OpenAI'
          name: chatGptModelName
          version: '0301'
        }
        capacity: chatGptDeploymentCapacity
      }
    ]
  }
}

output AZURE_OPENAI_SERVICE string = openai.outputs.name
output AZURE_OPENAI_ENDPOINT string = openai.outputs.endpoint
output AZURE_OPENAI_GPT_DEPLOYMENT string = gptDeploymentName
output AZURE_OPENAI_CHATGPT_DEPLOYMENT string = chatGptDeploymentName
