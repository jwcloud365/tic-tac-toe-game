@echo off
REM This script deploys the Tic-Tac-Toe application infrastructure to Azure
REM using the Bicep template and parameters file, then deploys the application code

REM Variables
set RESOURCE_GROUP=tictactoegroup3
set LOCATION=northeurope
set TEMPLATE_FILE=main.bicep
set PARAMETERS_FILE=main.parameters.json

REM Ask if user wants to deploy both infrastructure and application
set /P DEPLOY_BOTH="Do you want to deploy both infrastructure and application? (y/n): "
if /I not "%DEPLOY_BOTH%" == "y" (
  set DEPLOY_BOTH=n
)

REM Create a new resource group
echo Creating resource group %RESOURCE_GROUP% in %LOCATION%...
call az group create --name %RESOURCE_GROUP% --location %LOCATION%

REM Deploy the Bicep template
echo Deploying Tic-Tac-Toe infrastructure...
call az deployment group create ^
  --resource-group %RESOURCE_GROUP% ^
  --template-file %TEMPLATE_FILE% ^
  --parameters @%PARAMETERS_FILE%

REM Get deployment outputs
echo Deployment completed. Getting outputs...
for /f "tokens=*" %%a in ('az deployment group list --resource-group %RESOURCE_GROUP% --query "[0].name" -o tsv') do set DEPLOYMENT_NAME=%%a

for /f "tokens=*" %%a in ('az deployment group show --resource-group %RESOURCE_GROUP% --name %DEPLOYMENT_NAME% --query "properties.outputs.webAppName.value" -o tsv') do set WEBAPP_NAME=%%a

for /f "tokens=*" %%a in ('az deployment group show --resource-group %RESOURCE_GROUP% --name %DEPLOYMENT_NAME% --query "properties.outputs.webAppHostName.value" -o tsv') do set WEBAPP_HOSTNAME=%%a

echo Web App Name: %WEBAPP_NAME%
echo Web App Hostname: %WEBAPP_HOSTNAME%

REM Application deployment (if requested)
if /I "%DEPLOY_BOTH%" == "y" (
  echo Preparing to deploy application code...
  
  REM Create a temporary directory for deployment packaging
  set TEMP_DIR=%TEMP%\tictactoe_deploy
  if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"
  mkdir "%TEMP_DIR%"
  
  REM Copy application files to temporary directory
  echo Copying application files...
  xcopy app.py "%TEMP_DIR%\" /y
  xcopy requirements.txt "%TEMP_DIR%\" /y
  xcopy static\* "%TEMP_DIR%\static\" /s /i /y
  xcopy templates\* "%TEMP_DIR%\templates\" /s /i /y
  if exist run.sh copy run.sh "%TEMP_DIR%\" /y
  
  REM Create deployment package
  echo Creating deployment package...
  cd "%TEMP_DIR%"
  powershell Compress-Archive -Path * -DestinationPath ..\app.zip -Force
  cd %~dp0
  copy "%TEMP%\app.zip" .
  
  REM Deploy the application to Azure
  echo Deploying application code to Azure...
  call az webapp deployment source config-zip ^
    --resource-group %RESOURCE_GROUP% ^
    --name %WEBAPP_NAME% ^
    --src app.zip
  
  REM Configure startup command
  echo Setting startup command...
  call az webapp config set ^
    --resource-group %RESOURCE_GROUP% ^
    --name %WEBAPP_NAME% ^
    --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
  
  REM Clean up temporary directory and zip file
  rd /s /q "%TEMP_DIR%"
  del app.zip
  
  echo Application deployed successfully!
  echo You can access your app at: https://%WEBAPP_HOSTNAME%
) else (
  echo Infrastructure deployment completed.
  echo You can access your app at: https://%WEBAPP_HOSTNAME%
  echo.
  echo To deploy your application code later, use:
  echo az webapp deployment source config-zip --resource-group %RESOURCE_GROUP% --name %WEBAPP_NAME% --src app.zip
)

pause
