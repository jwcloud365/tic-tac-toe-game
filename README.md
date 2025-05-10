# Deploy Tic-Tac-Toe Infrastructure

This file contains instructions for deploying the Tic-Tac-Toe application infrastructure using the Bicep template.

## Overview

The `main.bicep` file creates the following resources:
- Network Security Group (NSG) with HTTP/HTTPS access restrictions
- App Service Plan (Linux)
- Web App (Python 3.10)

These resources replicate the existing application infrastructure (`tictactoegroup2`) but with new names and in a new resource group.

## Parameters

The template accepts the following parameters:

- **location**: Azure region where resources will be deployed (defaults to resource group location)
- **resourceGroupName**: Name of the resource group (defaults to current resource group)
- **appNamePrefix**: Prefix for naming all resources
- **allowedIpAddress**: IP address that will be allowed to access the app (for security restrictions)
- **linuxFxVersion**: Runtime stack for the application (defaults to 'PYTHON|3.10')
- **skuName**: App Service Plan SKU name (defaults to 'B1')
- **skuTier**: App Service Plan SKU tier (defaults to 'Basic')

## Deployment Steps

1. First, create a new resource group for the second Tic-Tac-Toe instance:

```bash
az group create --name tictactoegroup3 --location northeurope
```

2. Deploy the Bicep template using the Azure CLI:

```bash
az deployment group create \
  --resource-group tictactoegroup3 \
  --template-file main.bicep \
  --parameters appNamePrefix=tictactoe-new allowedIpAddress=YOUR_IP_ADDRESS
```

Replace `YOUR_IP_ADDRESS` with your actual IP address.

3. Deploy the application code using the instructions in the "Application Deployment" section below.

## Notes

- The template includes security restrictions that will only allow access from the specified IP address.
- The web app name includes a unique string generated from the resource group ID to ensure uniqueness.
- The template uses the Basic (B1) App Service Plan by default, matching the existing infrastructure.

## Application Deployment

You have several options for deploying the Tic-Tac-Toe application:

### Option 1: Automated Deployment Scripts

The repository includes scripts to automate both the infrastructure and application deployment:

#### For Linux/Mac users:
```bash
# Make the script executable
chmod +x deploy.sh

# Run the script
./deploy.sh
```

#### For Windows users:
```cmd
# Run the batch script
deploy.bat
```

These scripts will:
1. Create a resource group in Azure
2. Deploy the infrastructure using the Bicep template
3. Ask if you want to deploy the application code as well
4. If yes, package and deploy the application code
5. Configure the proper startup command

### Option 2: Manual ZIP Deployment

If you prefer to deploy the application manually:

1. Create a deployment ZIP package of your application:

```bash
# Navigate to your application directory
cd /path/to/application

# Create deployment package
zip -r app.zip app.py static/ templates/ requirements.txt
```

2. Deploy the ZIP package to Azure:

```bash
# Get the name of your deployed web app
WEBAPP_NAME=$(az deployment group show \
  --resource-group tictactoegroup3 \
  --name [deployment-name] \
  --query "properties.outputs.webAppName.value" -o tsv)

# Deploy the ZIP file
az webapp deployment source config-zip \
  --resource-group tictactoegroup3 \
  --name $WEBAPP_NAME \
  --src app.zip
```

### Option 3: GitHub Actions

1. Push your code to a GitHub repository.

2. Set up GitHub Actions deployment credentials:

```bash
# Get publishing credentials for the web app
az webapp deployment list-publishing-credentials \
  --resource-group tictactoegroup3 \
  --name $WEBAPP_NAME

# Note the publishingUserName and publishingPassword from the output
```

3. Add these credentials as GitHub secrets in your repository:
   - `AZURE_WEBAPP_NAME`: Your Azure Web App name
   - `AZURE_WEBAPP_PUBLISH_PROFILE`: The publishing profile content

4. Create a GitHub workflow file at `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Azure Web App

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: ${{ secrets.AZURE_WEBAPP_NAME }}
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

### Option 4: Local Git Deployment

1. Configure local Git deployment for your web app:

```bash
# Configure local Git deployment
az webapp deployment source config-local-git \
  --resource-group tictactoegroup3 \
  --name $WEBAPP_NAME
```

2. Add the Azure remote to your local Git repository:

```bash
# Get the Git URL
GIT_URL=$(az webapp deployment list-publishing-credentials \
  --resource-group tictactoegroup3 \
  --name $WEBAPP_NAME \
  --query scmUri -o tsv)/site/repository

# Add the remote
git remote add azure $GIT_URL

# Push your code
git push azure main
```

### Configure Startup Command

Make sure your web app is configured with the proper startup command:

```bash
# Set the startup command for the web app
az webapp config set \
  --resource-group tictactoegroup3 \
  --name $WEBAPP_NAME \
  --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
```

This will ensure that your Flask application starts correctly when deployed.

## Verifying the Deployment

The repository includes a Python script that can verify your deployment:

```bash
# Install required packages
pip install argparse requests

# Run the verification script
python verify_deployment.py --resource-group tictactoegroup3
```

This script will:
1. Check that all resources have been created successfully
2. Verify that the web app is running and properly configured
3. Test the application functionality by making API calls
4. Provide a detailed report of test results

For more options:
```bash
python verify_deployment.py --help
```

## Parameters File

The deployment uses a parameters file (`main.parameters.json`) for easier configuration:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "appNamePrefix": {
      "value": "tictactoe-new"
    },
    "allowedIpAddress": {
      "value": "YOUR_IP_ADDRESS"
    },
    "location": {
      "value": "northeurope"
    },
    "skuName": {
      "value": "B1"
    },
    "skuTier": {
      "value": "Basic"
    },
    "linuxFxVersion": {
      "value": "PYTHON|3.10"
    }
  }
}
```

You can modify this file to customize your deployment, then deploy using:

```bash
az deployment group create \
  --resource-group tictactoegroup3 \
  --template-file main.bicep \
  --parameters main.parameters.json
```
