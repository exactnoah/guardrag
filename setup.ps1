# setup.ps1 - One-time setup script for Haystack RAG project

Write-Host "Setting up Haystack RAG environment..." -ForegroundColor Green

# Check if venv exists
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Delete it? (y/n)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq 'y') {
        Remove-Item -Recurse -Force venv
        Write-Host "Removed existing venv" -ForegroundColor Green
    } else {
        Write-Host "Keeping existing venv. Exiting." -ForegroundColor Yellow
        exit
    }
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
py -3.14 -m venv venv

# Activate it
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet

# Install requirements
Write-Host "Installing dependencies (this may take 5-10 minutes)..." -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "To activate the environment in future sessions, run:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To test the setup, run:" -ForegroundColor Yellow
Write-Host "  python rag_pipeline.py" -ForegroundColor White