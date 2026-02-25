# setup.ps1 - One-time setup script for Haystack RAG project
Write-Host "Installing Ollama and Mistral:7b (if not already exists)..." -ForegroundColor Cyan
py .\setup_materials\install_llm.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "install.py failed. Exiting setup." -ForegroundColor Red
    exit 1
}

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

# Install python-docx
Write-Host "Installing python-docx..." -ForegroundColor Cyan
pip install python-docx

# Install requirements
Write-Host "Installing dependencies (this may take 5-10 minutes)..." -ForegroundColor Cyan
#pip install -e .[haystack]
pip install -r .\setup_materials\requirements.txt

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "To activate the environment in future sessions, run:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To test the setup, run:" -ForegroundColor Yellow
Write-Host "  python .\pipelines\rag_pipeline.py" -ForegroundColor White