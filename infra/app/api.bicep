param name string
param location string = resourceGroup().location
param tags object = {}

param allowedOrigins array = []
param applicationInsightsName string = ''
param appServicePlanId string
param appSettings object = {}
param keyVaultName string
param serviceName string = 'api'
param storageAccountName string
param openAiAccountName string
param openAiResourceGroupName string

module api '../core/host/functions.bicep' = {
  name: '${serviceName}-functions-python-module'
  params: {
    name: name
    location: location
    tags: union(tags, { 'azd-service-name': serviceName })
    allowedOrigins: allowedOrigins
    alwaysOn: false
    appSettings: union(appSettings, {
        AZURE_OPENAI_KEY: openai.listKeys().key1
      })
    applicationInsightsName: applicationInsightsName
    appServicePlanId: appServicePlanId
    keyVaultName: keyVaultName
    //py
    numberOfWorkers: 1
    minimumElasticInstanceCount: 0
    //--py
    runtimeName: 'python'
    runtimeVersion: '3.9'
    storageAccountName: storageAccountName
    scmDoBuildDuringDeployment: false
  }
}

resource openai 'Microsoft.CognitiveServices/accounts@2023-05-01' existing = {
  name: openAiAccountName
  scope: resourceGroup(openAiResourceGroupName)
}

output SERVICE_API_IDENTITY_PRINCIPAL_ID string = api.outputs.identityPrincipalId
output SERVICE_API_NAME string = api.outputs.name
output SERVICE_API_URI string = api.outputs.uri
