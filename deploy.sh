#!/bin/bash

# This script deploys the Tic-Tac-Toe application infrastructure to Azure
# using the Bicep template and parameters file, then deploys the application code

# Variables
RESOURCE_GROUP="tictactoegroup3"
LOCATION="northeurope"
TEMPLATE_FILE="main.bicep"
PARAMETERS_FILE="main.parameters.json"

# Ask if user wants to deploy both infrastructure and application
read -p "Do you want to deploy both infrastructure and application? (y/n): " DEPLOY_BOTH
if [[ "$DEPLOY_BOTH" != "y" && "$DEPLOY_BOTH" != "Y" ]]; then
  DEPLOY_BOTH="n"
fi

# Create a new resource group
echo "Creating resource group $RESOURCE_GROUP in $LOCATION..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Deploy the Bicep template
echo "Deploying Tic-Tac-Toe infrastructure..."
az deployment group create \
  --resource-group $RESOURCE_GROUP \
  --template-file $TEMPLATE_FILE \
  --parameters @$PARAMETERS_FILE

# Get deployment outputs
echo "Deployment completed. Getting outputs..."
WEBAPP_NAME=$(az deployment group show \
  --resource-group $RESOURCE_GROUP \
  --name $(az deployment group list --resource-group $RESOURCE_GROUP --query "[0].name" -o tsv) \
  --query "properties.outputs.webAppName.value" -o tsv)

WEBAPP_HOSTNAME=$(az deployment group show \
  --resource-group $RESOURCE_GROUP \
  --name $(az deployment group list --resource-group $RESOURCE_GROUP --query "[0].name" -o tsv) \
  --query "properties.outputs.webAppHostName.value" -o tsv)

echo "Web App Name: $WEBAPP_NAME"
echo "Web App Hostname: $WEBAPP_HOSTNAME"

# Application deployment (if requested)
if [[ "$DEPLOY_BOTH" == "y" || "$DEPLOY_BOTH" == "Y" ]]; then
  echo "Preparing to deploy application code..."
  
  # Create a temporary directory for deployment packaging
  TEMP_DIR=$(mktemp -d)
  
  # Copy application files to temporary directory
  echo "Copying application files..."
  cp -r app.py requirements.txt static/ templates/ run.sh $TEMP_DIR/
  
  # Create deployment package
  echo "Creating deployment package..."
  cd $TEMP_DIR
  zip -r ../app.zip *
  cd -
  
  # Deploy the application to Azure
  echo "Deploying application code to Azure..."
  az webapp deployment source config-zip \
    --resource-group $RESOURCE_GROUP \
    --name $WEBAPP_NAME \
    --src app.zip
  
  # Configure startup command
  echo "Setting startup command..."
  az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $WEBAPP_NAME \
    --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
  
  # Clean up temporary directory and zip file
  rm -rf $TEMP_DIR app.zip
  
  echo "Application deployed successfully!"
  echo "You can access your app at: https://$WEBAPP_HOSTNAME"
else
  echo "Infrastructure deployment completed."
  echo "You can access your app at: https://$WEBAPP_HOSTNAME"
  echo ""
  echo "To deploy your application code later, use:"
  echo "az webapp deployment source config-zip --resource-group $RESOURCE_GROUP --name $WEBAPP_NAME --src app.zip"
fi
