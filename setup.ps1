# setup.ps1 - Windows wrapper for the consolidated GuardRag installer

Write-Host "Starting GuardRag setup..." -ForegroundColor Cyan

$launchArg = ""
$launchChoice = Read-Host "Launch GuardRag GUI automatically after setup? (y/n)"
if ($launchChoice -eq "y") {
    $launchArg = "--launch-app"
}

py .\scripts\install.py --model mistral:7b $launchArg

if ($LASTEXITCODE -ne 0) {
    Write-Host "GuardRag setup failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "GuardRag setup finished successfully." -ForegroundColor Green