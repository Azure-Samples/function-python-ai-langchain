param principalID string
param principalType string = 'ServicePrincipal' // Workaround for https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-template#new-service-principal
param roleDefinitionID string
param aiResourceName string

resource cognitiveService 'Microsoft.CognitiveServices/accounts@2023-05-01' existing = {
  name: aiResourceName
}

// Allow access from API to this resource using a managed identity and least priv role grants
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(cognitiveService.id, principalID, roleDefinitionID)
  scope: cognitiveService
  properties: {
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionID)
    principalId: principalID
    principalType: principalType 
  }
}

output ROLE_ASSIGNMENT_NAME string = roleAssignment.name
