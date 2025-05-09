# Add Flask to Windows PATH
# Run this script as Administrator

# Add Python main directories to PATH
$pythonPath = "C:\Python313"
$pythonScriptsPath = "C:\Python313\Scripts"
$userScriptsPath = "C:\Users\HP\AppData\Roaming\Python\Python313\Scripts"

# Get current PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Check if paths are already in PATH
$addPython = $false
if (-not $currentPath.Contains($pythonPath)) {
    $currentPath += ";$pythonPath"
    $addPython = $true
}

$addPythonScripts = $false
if (-not $currentPath.Contains($pythonScriptsPath)) {
    $currentPath += ";$pythonScriptsPath"
    $addPythonScripts = $true
}

$addUserScripts = $false
if (-not $currentPath.Contains($userScriptsPath)) {
    $currentPath += ";$userScriptsPath"
    $addUserScripts = $true
}

# Update PATH if changes were made
if ($addPython -or $addPythonScripts -or $addUserScripts) {
    [Environment]::SetEnvironmentVariable("Path", $currentPath, "User")
    Write-Host "Python paths were added to your PATH environment variable."
    Write-Host "Please restart your terminal for changes to take effect."
} else {
    Write-Host "All Python paths are already in your PATH environment variable."
}
