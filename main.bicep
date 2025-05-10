/*
   Tic-Tac-Toe Application Infrastructure Bicep Template
   This template creates a complete environment for the Tic-Tac-Toe application including:
   - Network Security Group (NSG) with HTTP/HTTPS access restrictions
   - App Service Plan (Linux)
   - Web App (Python 3.10)
*/

// Parameters
param location string = resourceGroup().location
param resourceGroupName string = resourceGroup().name
param appNamePrefix string
param allowedIpAddress string
param linuxFxVersion string = 'PYTHON|3.10'
param skuName string = 'B1'
param skuTier string = 'Basic'

// Variables
var appServicePlanName = '${appNamePrefix}-plan'
var webAppName = '${appNamePrefix}-game-${uniqueString(resourceGroup().id)}'
var nsgName = '${appNamePrefix}-nsg'

// Network Security Group
resource networkSecurityGroup 'Microsoft.Network/networkSecurityGroups@2023-05-01' = {
  name: nsgName
  location: location
  properties: {
    securityRules: [
      {
        name: 'Allow-HTTP-HTTPS'
        properties: {
          priority: 100
          access: 'Allow'
          direction: 'Inbound'
          protocol: 'Tcp'
          sourceAddressPrefix: allowedIpAddress
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRanges: [
            '80'
            '443'
          ]
          description: 'Allow HTTP and HTTPS traffic from specific IP address'
        }
      }
      {
        name: 'Deny-HTTP-HTTPS'
        properties: {
          priority: 110
          access: 'Deny'
          direction: 'Inbound'
          protocol: 'Tcp'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRanges: [
            '80'
            '443'
          ]
          description: 'Deny HTTP and HTTPS traffic from all other sources'
        }
      }
    ]
  }
}

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: skuName
    tier: skuTier
  }
  kind: 'linux'
  properties: {
    reserved: true // Required for Linux plan
  }
}

// Web App
resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: webAppName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    clientAffinityEnabled: true
    siteConfig: {
      linuxFxVersion: linuxFxVersion
      alwaysOn: false // Basic plan doesn't support always on
      http20Enabled: true
      minTlsVersion: '1.2'
      ipSecurityRestrictions: [
        {
          ipAddress: '${allowedIpAddress}/32'
          action: 'Allow'
          priority: 100
          name: 'Allow specific IP'
          description: 'Allow specific IP address'
        }
      ]
      scmIpSecurityRestrictions: [
        {
          ipAddress: '${allowedIpAddress}/32'
          action: 'Allow'
          priority: 100
          name: 'Allow specific IP for SCM'
          description: 'Allow specific IP address for deployment'
        }
      ]
    }
  }
}

// Outputs
output webAppName string = webApp.name
output webAppHostName string = webApp.properties.defaultHostName
output appServicePlanName string = appServicePlan.name
output nsgName string = networkSecurityGroup.name
