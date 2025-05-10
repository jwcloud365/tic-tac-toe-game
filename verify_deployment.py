#!/usr/bin/env python
"""
Verify TicTacToe App Deployment

This script verifies that the Tic-Tac-Toe application deployed to Azure
is working correctly by running a series of tests against the deployed
application and infrastructure.
"""

import argparse
import json
import re
import sys
import time
from typing import Dict, List, Optional, Tuple
import urllib.request
import urllib.error
import subprocess

class DeploymentVerifier:
    """Verifies the deployment of TicTacToe application in Azure."""
    
    def __init__(self, resource_group: str, location: str = None, webapp_name: str = None) -> None:
        """
        Initialize the verifier with resource group and optional webapp name.
        
        Args:
            resource_group (str): The Azure resource group name.
            location (str, optional): The Azure location. Defaults to None.
            webapp_name (str, optional): The name of the web app. If not provided,
                                         it will be retrieved from the deployment outputs.
        """
        self.resource_group = resource_group
        self.location = location
        self.webapp_name = webapp_name
        self.webapp_hostname = None
        self.tests_passed = 0
        self.tests_failed = 0
        
    def run(self) -> None:
        """Run all verification tests."""
        self.print_header("Tic-Tac-Toe Deployment Verification")
        
        # Get deployment outputs if webapp_name is not provided
        if not self.webapp_name:
            try:
                self.get_deployment_outputs()
            except Exception as e:
                self.print_error(f"Failed to get deployment outputs: {str(e)}")
                sys.exit(1)
        
        # Run verification tests
        self.verify_resource_group()
        self.verify_infrastructure()
        self.verify_webapp_running()
        self.verify_webapp_configuration()
        self.verify_app_functionality()
        
        # Print summary
        self.print_summary()
    
    def get_deployment_outputs(self) -> None:
        """Get the deployment outputs from Azure."""
        print("Getting deployment outputs...")
        
        try:
            # Get the latest deployment name
            deployment_name = self.run_az_command([
                "deployment", "group", "list",
                "--resource-group", self.resource_group,
                "--query", "[0].name",
                "-o", "tsv"
            ]).strip()
            
            # Get webapp name from outputs
            self.webapp_name = self.run_az_command([
                "deployment", "group", "show",
                "--resource-group", self.resource_group,
                "--name", deployment_name,
                "--query", "properties.outputs.webAppName.value",
                "-o", "tsv"
            ]).strip()
            
            # Get webapp hostname from outputs
            self.webapp_hostname = self.run_az_command([
                "deployment", "group", "show",
                "--resource-group", self.resource_group,
                "--name", deployment_name,
                "--query", "properties.outputs.webAppHostName.value",
                "-o", "tsv"
            ]).strip()
            
            print(f"  Web App Name: {self.webapp_name}")
            print(f"  Web App Hostname: {self.webapp_hostname}")
        except Exception as e:
            raise Exception(f"Failed to get deployment outputs: {str(e)}")
    
    def verify_resource_group(self) -> None:
        """Verify resource group exists."""
        self.print_test_header("Verifying resource group")
        
        try:
            result = self.run_az_command([
                "group", "show",
                "--name", self.resource_group
            ])
            data = json.loads(result)
            self.assert_test(data["name"] == self.resource_group, 
                           f"Resource group {self.resource_group} exists")
        except Exception as e:
            self.assert_test(False, f"Resource group check failed: {str(e)}")
    
    def verify_infrastructure(self) -> None:
        """Verify all required infrastructure components exist."""
        self.print_test_header("Verifying infrastructure components")
        
        # Check App Service Plan
        try:
            plans = self.run_az_command([
                "appservice", "plan", "list",
                "--resource-group", self.resource_group,
                "--query", "[].name",
                "-o", "json"
            ])
            plans_data = json.loads(plans)
            self.assert_test(len(plans_data) > 0, "App Service Plan exists")
        except Exception as e:
            self.assert_test(False, f"App Service Plan check failed: {str(e)}")
        
        # Check Network Security Group
        try:
            nsgs = self.run_az_command([
                "network", "nsg", "list",
                "--resource-group", self.resource_group,
                "--query", "[].name",
                "-o", "json"
            ])
            nsgs_data = json.loads(nsgs)
            self.assert_test(len(nsgs_data) > 0, "Network Security Group exists")
        except Exception as e:
            self.assert_test(False, f"Network Security Group check failed: {str(e)}")
        
        # Check Web App
        try:
            webapp = self.run_az_command([
                "webapp", "show",
                "--resource-group", self.resource_group,
                "--name", self.webapp_name
            ])
            webapp_data = json.loads(webapp)
            self.assert_test(webapp_data["name"] == self.webapp_name, "Web App exists")
        except Exception as e:
            self.assert_test(False, f"Web App check failed: {str(e)}")
    
    def verify_webapp_running(self) -> None:
        """Verify web app is running and accessible."""
        self.print_test_header("Verifying web app is running")
        
        url = f"https://{self.webapp_hostname}"
        max_retries = 5
        retry_delay = 10
        
        for attempt in range(max_retries):
            try:
                print(f"  Attempt {attempt+1}/{max_retries}: Accessing {url}")
                response = urllib.request.urlopen(url, timeout=30)
                content = response.read().decode('utf-8')
                
                self.assert_test(response.getcode() == 200, "Web App returns 200 OK")
                self.assert_test("Tic-Tac-Toe" in content, "Web App contains 'Tic-Tac-Toe' title")
                return
            except urllib.error.HTTPError as e:
                print(f"  HTTP error: {e.code} - {e.reason}")
                if attempt == max_retries - 1:
                    self.assert_test(False, f"Web App is not accessible after {max_retries} attempts")
            except Exception as e:
                print(f"  Error: {str(e)}")
                if attempt == max_retries - 1:
                    self.assert_test(False, f"Web App is not accessible: {str(e)}")
            
            print(f"  Waiting {retry_delay} seconds before next attempt...")
            time.sleep(retry_delay)
    
    def verify_webapp_configuration(self) -> None:
        """Verify web app configuration."""
        self.print_test_header("Verifying web app configuration")
        
        try:
            # Verify HTTPS Only
            config = self.run_az_command([
                "webapp", "show",
                "--resource-group", self.resource_group,
                "--name", self.webapp_name
            ])
            config_data = json.loads(config)
            self.assert_test(config_data["httpsOnly"] == True, "HTTPS Only is enabled")
            
            # Verify Python version
            site_config = self.run_az_command([
                "webapp", "config", "show",
                "--resource-group", self.resource_group,
                "--name", self.webapp_name
            ])
            site_config_data = json.loads(site_config)
            self.assert_test(site_config_data["linuxFxVersion"].startswith("PYTHON"), 
                           "Python runtime is configured")
            self.assert_test(site_config_data["minTlsVersion"] == "1.2", 
                           "TLS version is set to 1.2 minimum")
        except Exception as e:
            self.assert_test(False, f"Configuration check failed: {str(e)}")
    
    def verify_app_functionality(self) -> None:
        """Verify application functionality."""
        self.print_test_header("Verifying application functionality")
        
        base_url = f"https://{self.webapp_hostname}"
        
        try:
            # Test reset endpoint
            reset_url = f"{base_url}/reset"
            headers = {'Content-Type': 'application/json'}
            data = json.dumps({"firstPlayer": "X"}).encode('utf-8')
            
            req = urllib.request.Request(reset_url, data=data, headers=headers, method='POST')
            response = urllib.request.urlopen(req, timeout=30)
            reset_data = json.loads(response.read().decode('utf-8'))
            
            self.assert_test("board" in reset_data, "Reset endpoint returns game board")
            self.assert_test(reset_data["currentPlayer"] == "X", "Reset sets correct player")
            
            # Test move endpoint
            move_url = f"{base_url}/move"
            move_data = json.dumps({"index": 0}).encode('utf-8')
            
            req = urllib.request.Request(move_url, data=move_data, headers=headers, method='POST')
            response = urllib.request.urlopen(req, timeout=30)
            game_data = json.loads(response.read().decode('utf-8'))
            
            self.assert_test(game_data["board"][0] == "X", "Move endpoint updates game board")
            self.assert_test("computerMove" in game_data, "Computer makes counter-move")
            
        except Exception as e:
            self.assert_test(False, f"Application functionality test failed: {str(e)}")
    
    def run_az_command(self, args: List[str]) -> str:
        """
        Run an Azure CLI command and return its output.
        
        Args:
            args: List of command arguments
            
        Returns:
            Command output as string
        """
        cmd = ["az"] + args
        try:
            return subprocess.check_output(cmd, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            print(f"Azure CLI command failed: {' '.join(cmd)}")
            print(f"Error: {e.output}")
            raise
    
    def assert_test(self, condition: bool, message: str) -> None:
        """
        Assert a test condition and update test counts.
        
        Args:
            condition: Test condition to check
            message: Test message to display
        """
        if condition:
            print(f"  ✅ {message}")
            self.tests_passed += 1
        else:
            print(f"  ❌ {message}")
            self.tests_failed += 1
    
    def print_header(self, title: str) -> None:
        """Print a section header."""
        border = "=" * (len(title) + 4)
        print(f"\n{border}")
        print(f"  {title}  ")
        print(f"{border}\n")
    
    def print_test_header(self, title: str) -> None:
        """Print a test section header."""
        print(f"\n>> {title}:")
    
    def print_summary(self) -> None:
        """Print test summary."""
        total = self.tests_passed + self.tests_failed
        self.print_header("Test Summary")
        print(f"Total tests:  {total}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_failed}")
        
        if self.tests_failed == 0:
            print("\n✅ All tests passed! Deployment verification successful.")
            print(f"You can access the app at: https://{self.webapp_hostname}")
        else:
            print(f"\n❌ {self.tests_failed} tests failed. See the output above for details.")

def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Verify TicTacToe application deployment in Azure")
    parser.add_argument("--resource-group", "-g", required=True, 
                        help="Azure resource group name")
    parser.add_argument("--location", "-l", help="Azure location")
    parser.add_argument("--webapp-name", "-w", help="Web app name")
    
    args = parser.parse_args()
    
    verifier = DeploymentVerifier(
        resource_group=args.resource_group,
        location=args.location,
        webapp_name=args.webapp_name
    )
    verifier.run()

if __name__ == "__main__":
    main()
