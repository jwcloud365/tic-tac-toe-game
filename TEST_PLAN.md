# Test Plan for Tic-Tac-Toe Infrastructure Deployment

This document outlines the test plan for the Tic-Tac-Toe infrastructure deployment using the Bicep template.

## Pre-Deployment Tests

1. **Template Validation**
   - Validate the Bicep template syntax:
     ```bash
     az bicep build --file main.bicep
     ```
   - Validate the deployment using a what-if operation:
     ```bash
     az deployment group what-if --resource-group tictactoegroup3 --template-file main.bicep --parameters @main.parameters.json
     ```

2. **Parameter Validation**
   - Ensure all required parameters are provided in the parameters file
   - Verify parameter values are within valid ranges

## Deployment Tests

1. **Resource Creation**
   - Verify all resources are created successfully
   - Check resource naming follows the pattern defined in the template
   - Validate dependencies are properly created in the correct order

2. **Network Security Group Configuration**
   - Validate inbound security rules are created with correct priorities
   - Confirm HTTP/HTTPS access is limited to the specified IP address
   - Test access from allowed IP address should succeed
   - Test access from other IP addresses should be denied

3. **App Service Plan Configuration**
   - Verify app service plan is created with the correct SKU
   - Confirm Linux configuration is applied
   - Validate reserved property is set to true for Linux

4. **Web App Configuration**
   - Verify Python 3.10 runtime is configured
   - Confirm HTTPS Only setting is enabled
   - Validate IP security restrictions are applied
   - Check TLS version is set to 1.2 minimum
   - Verify HTTP/2 is enabled

## Post-Deployment Tests

1. **Access Testing**
   - Test web app is accessible from the allowed IP address
   - Confirm access is denied from any other IP address
   - Verify SCM/Kudu site access restrictions work as expected

2. **Application Deployment**
   - Test deploying the Tic-Tac-Toe application to the web app
   - Verify application runs correctly after deployment
   - Test application functionality is identical to the original deployment

3. **Performance Validation**
   - Validate the application performs similarly to the original deployment
   - Check response times are within acceptable ranges

## Cleanup Testing

1. **Resource Deletion**
   - Verify resources can be cleanly deleted when no longer needed
   - Test that deleting the resource group removes all deployed resources

## Security Verification

1. **IP Restriction Testing**
   - Verify only the specified IP address can access the web app
   - Confirm SCM site is also protected by IP restrictions
   - Test that changing the allowed IP updates the access restrictions

2. **HTTPS Enforcement**
   - Confirm HTTP requests are redirected to HTTPS
   - Verify TLS 1.2 is enforced as the minimum TLS version
