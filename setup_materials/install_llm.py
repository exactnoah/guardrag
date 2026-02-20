#!/usr/bin/env python3
"""
Minimal Ollama + Mistral 7B Setup Script
"""

import shutil
import subprocess
import sys
import platform


MODEL_NAME = "mistral:7b"


def check_ollama_installed() -> bool:
    """Check if Ollama is installed."""
    if shutil.which("ollama"):
        print("✓ Ollama is installed")
        return True

    print("✗ Ollama is not installed.")
    print("Download it from: https://ollama.com/download")
    return False


def pull_model(model_name: str) -> bool:
    """Pull Mistral 7B model using Ollama."""
    try:
        subprocess.run(["ollama", "pull", model_name], check=True)
        print(f"✓ Model '{model_name}' pulled successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to pull model")
        return False


def main():
    if not check_ollama_installed():
        sys.exit(1)

    print(f"Pulling model: {MODEL_NAME}")
    pull_model(MODEL_NAME)


if __name__ == "__main__":
    main()