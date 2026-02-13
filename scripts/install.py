#!/usr/bin/env python3
"""
GuardRag Installation Script

Cross-platform installer that:
1. Creates virtual environment
2. Installs Python dependencies (including Haystack)
3. Sets up environment configuration
4. Pulls Ollama models
5. Validates the installation

Usage:
    python scripts/install.py [--skip-models] [--model MODEL_NAME]
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
VENV_DIR = PROJECT_ROOT / ".venv"
ENV_FILE = PROJECT_ROOT / ".env"
ENV_EXAMPLE = PROJECT_ROOT / ".env.example"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"
OLLAMA_MODELS_DIR = PROJECT_ROOT / ".ollama" / "models"

DEFAULT_MODEL = "llama3.1:8b"
OLLAMA_HOST = "http://localhost:11434"

# Colors for terminal output
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def print_step(msg: str) -> None:
    print(f"\n{Colors.BLUE}{Colors.BOLD}==>{Colors.RESET} {msg}")

def print_success(msg: str) -> None:
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")

def print_warning(msg: str) -> None:
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")

def print_error(msg: str) -> None:
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")

# =============================================================================
# System Checks
# =============================================================================

def check_python_version() -> bool:
    """Ensure Python 3.10+ is available."""
    print_step("Checking Python version...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python 3.10+ required, found {version.major}.{version.minor}")
        return False

def check_ollama_installed() -> bool:
    """Check if Ollama is installed and accessible."""
    print_step("Checking Ollama installation...")
    
    ollama_path = shutil.which("ollama")
    if ollama_path:
        print_success(f"Ollama found at: {ollama_path}")
        return True
    
    # Check common Windows locations
    if platform.system() == "Windows":
        common_paths = [
            Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama.exe",
            Path("C:/Program Files/Ollama/ollama.exe"),
        ]
        for path in common_paths:
            if path.exists():
                print_success(f"Ollama found at: {path}")
                return True
    
    print_warning("Ollama not found in PATH")
    return False

def check_ollama_running() -> bool:
    """Check if Ollama server is running."""
    import urllib.request
    import urllib.error
    
    try:
        req = urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if req.status == 200:
            print_success("Ollama server is running")
            return True
    except (urllib.error.URLError, urllib.error.HTTPError):
        pass
    
    print_warning("Ollama server not responding")
    return False

# =============================================================================
# Virtual Environment
# =============================================================================

def create_virtualenv() -> bool:
    """Create virtual environment in project root."""
    print_step(f"Setting up virtual environment at {VENV_DIR}...")
    
    if VENV_DIR.exists():
        print_warning("Virtual environment already exists, skipping creation")
        return True
    
    try:
        subprocess.run(
            [sys.executable, "-m", "venv", str(VENV_DIR)],
            check=True,
            capture_output=True
        )
        print_success("Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {e}")
        return False

def get_venv_python() -> Path:
    """Get path to Python in virtual environment."""
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"

def get_venv_pip() -> Path:
    """Get path to pip in virtual environment."""
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "pip.exe"
    return VENV_DIR / "bin" / "pip"

# =============================================================================
# Dependencies
# =============================================================================

def install_dependencies() -> bool:
    """Install Python dependencies from requirements.txt."""
    print_step("Installing Python dependencies...")
    
    pip_path = get_venv_pip()
    
    if not pip_path.exists():
        print_error(f"pip not found at {pip_path}")
        return False
    
    try:
        # Upgrade pip first
        subprocess.run(
            [str(pip_path), "install", "--upgrade", "pip"],
            check=True,
            capture_output=True
        )
        
        # Install requirements
        subprocess.run(
            [str(pip_path), "install", "-r", str(REQUIREMENTS_FILE)],
            check=True
        )
        print_success("Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False

# =============================================================================
# Environment Configuration
# =============================================================================

def setup_environment() -> bool:
    """Copy .env.example to .env if not exists."""
    print_step("Setting up environment configuration...")
    
    if ENV_FILE.exists():
        print_warning(".env already exists, skipping")
        return True
    
    if not ENV_EXAMPLE.exists():
        print_error(".env.example not found")
        return False
    
    try:
        shutil.copy(ENV_EXAMPLE, ENV_FILE)
        print_success(f"Created {ENV_FILE}")
        return True
    except Exception as e:
        print_error(f"Failed to create .env: {e}")
        return False

def setup_ollama_models_dir() -> bool:
    """Create local Ollama models directory."""
    print_step("Setting up Ollama models directory...")
    
    try:
        OLLAMA_MODELS_DIR.mkdir(parents=True, exist_ok=True)
        print_success(f"Models directory: {OLLAMA_MODELS_DIR}")
        return True
    except Exception as e:
        print_error(f"Failed to create models directory: {e}")
        return False

# =============================================================================
# Ollama Models
# =============================================================================

def pull_ollama_model(model_name: str) -> bool:
    """Pull an Ollama model."""
    print_step(f"Pulling Ollama model: {model_name}...")
    
    # Set custom models directory
    env = os.environ.copy()
    env["OLLAMA_MODELS"] = str(OLLAMA_MODELS_DIR)
    
    try:
        result = subprocess.run(
            ["ollama", "pull", model_name],
            env=env,
            check=True
        )
        print_success(f"Model {model_name} pulled successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to pull model: {e}")
        return False
    except FileNotFoundError:
        print_error("Ollama command not found")
        return False

# =============================================================================
# Validation
# =============================================================================

def validate_installation() -> bool:
    """Validate that key components are working."""
    print_step("Validating installation...")
    
    python_path = get_venv_python()
    all_ok = True
    
    # Check key imports
    imports_to_check = [
        ("fastapi", "FastAPI"),
        ("haystack", "Haystack"),
        ("sentence_transformers", "SentenceTransformers"),
    ]
    
    for module, name in imports_to_check:
        try:
            result = subprocess.run(
                [str(python_path), "-c", f"import {module}"],
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0:
                print_success(f"{name} import OK")
            else:
                print_warning(f"{name} import failed")
                all_ok = False
        except subprocess.TimeoutExpired:
            print_warning(f"{name} import timed out")
            all_ok = False
    
    return all_ok

# =============================================================================
# Main
# =============================================================================

def print_banner() -> None:
    print(f"""
{Colors.BOLD}╔═══════════════════════════════════════════════╗
║           GuardRag Installer v1.0             ║
╚═══════════════════════════════════════════════╝{Colors.RESET}
""")

def print_next_steps(ollama_installed: bool, ollama_running: bool) -> None:
    print(f"\n{Colors.BOLD}{'='*50}")
    print(f"Next Steps")
    print(f"{'='*50}{Colors.RESET}\n")
    
    step = 1
    
    if not ollama_installed:
        print(f"{step}. Install Ollama:")
        print(f"   Download from: https://ollama.com/download")
        print()
        step += 1
    
    if not ollama_running:
        print(f"{step}. Start Ollama server:")
        print(f"   Run: ollama serve")
        print()
        step += 1
    
    print(f"{step}. Activate virtual environment:")
    if platform.system() == "Windows":
        print(f"   .venv\\Scripts\\activate")
    else:
        print(f"   source .venv/bin/activate")
    print()
    step += 1
    
    print(f"{step}. Pull the model (if not done):")
    print(f"   ollama pull {DEFAULT_MODEL}")
    print()
    step += 1
    
    print(f"{step}. Start the API:")
    print(f"   python -m api.main")
    print()

def main() -> int:
    """Main installation entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="GuardRag Installer")
    parser.add_argument("--skip-models", action="store_true", 
                        help="Skip pulling Ollama models")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Model to pull (default: {DEFAULT_MODEL})")
    args = parser.parse_args()
    
    print_banner()
    
    # System checks
    if not check_python_version():
        return 1
    
    ollama_installed = check_ollama_installed()
    ollama_running = False
    if ollama_installed:
        ollama_running = check_ollama_running()
    
    # Setup steps
    if not create_virtualenv():
        return 1
    
    if not install_dependencies():
        return 1
    
    if not setup_environment():
        return 1
    
    if not setup_ollama_models_dir():
        return 1
    
    # Pull model if Ollama is running
    if not args.skip_models and ollama_running:
        pull_ollama_model(args.model)
    elif not args.skip_models:
        print_warning("Skipping model pull - Ollama not running")
    
    # Validation
    validate_installation()
    
    # Summary
    print_next_steps(ollama_installed, ollama_running)
    
    print(f"{Colors.GREEN}{Colors.BOLD}Installation complete!{Colors.RESET}\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
