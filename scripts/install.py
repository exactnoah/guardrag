#!/usr/bin/env python3
"""GuardRag installation orchestrator for local and installer-driven setup."""

import argparse
import os
import platform
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DEFAULT_MODEL = "mistral:7b"
DEFAULT_OLLAMA_HOST = "http://localhost:11434"


class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


@dataclass
class InstallPaths:
    install_root: Path
    venv_dir: Path
    docs_dir: Path
    data_dir: Path
    logs_dir: Path
    config_dir: Path
    env_file: Path
    env_example: Path
    ollama_models_dir: Path
    requirements_file: Path
    app_entrypoint: Path


def print_step(msg: str) -> None:
    print(f"\n{Colors.BLUE}{Colors.BOLD}==>{Colors.RESET} {msg}")


def print_success(msg: str) -> None:
    print(f"{Colors.GREEN}[OK]{Colors.RESET} {msg}")


def print_warning(msg: str) -> None:
    print(f"{Colors.YELLOW}[WARN]{Colors.RESET} {msg}")


def print_error(msg: str) -> None:
    print(f"{Colors.RED}[ERR]{Colors.RESET} {msg}")


def build_paths(install_root: Path) -> InstallPaths:
    req_candidates = [
        PROJECT_ROOT / "setup_materials" / "requirements.txt",
        PROJECT_ROOT / "requirements.txt",
    ]
    requirements_file = next((p for p in req_candidates if p.exists()), req_candidates[0])
    return InstallPaths(
        install_root=install_root,
        venv_dir=install_root / ".venv",
        docs_dir=install_root / "docs",
        data_dir=install_root / "data",
        logs_dir=install_root / "logs",
        config_dir=install_root / "config",
        env_file=install_root / ".env",
        env_example=PROJECT_ROOT / ".env.example",
        ollama_models_dir=install_root / ".ollama" / "models",
        requirements_file=requirements_file,
        app_entrypoint=PROJECT_ROOT / "pipelines" / "rag_pipeline.py",
    )


def check_python_version() -> bool:
    print_step("Checking Python version")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    print_error(f"Python 3.10+ required, found {version.major}.{version.minor}")
    return False


def find_ollama_command() -> Path | None:
    path = shutil.which("ollama")
    if path:
        return Path(path)
    if platform.system() == "Windows":
        candidates = [
            Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama.exe",
            Path("C:/Program Files/Ollama/ollama.exe"),
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
    return None


def check_ollama_installed() -> Path | None:
    print_step("Checking Ollama installation")
    ollama_cmd = find_ollama_command()
    if ollama_cmd:
        print_success(f"Ollama found at {ollama_cmd}")
        return ollama_cmd
    print_warning("Ollama not found. Install from https://ollama.com/download")
    return None


def check_ollama_running(ollama_host: str, timeout: int = 5) -> bool:
    import urllib.error
    import urllib.request

    try:
        req = urllib.request.urlopen(f"{ollama_host}/api/tags", timeout=timeout)
        if req.status == 200:
            return True
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return False
    return False


def wait_for_ollama(ollama_host: str, wait_seconds: int) -> bool:
    if check_ollama_running(ollama_host):
        print_success("Ollama server is running")
        return True
    if wait_seconds <= 0:
        print_warning("Ollama server not responding")
        return False

    print_step(f"Waiting up to {wait_seconds}s for Ollama server")
    deadline = time.time() + wait_seconds
    while time.time() < deadline:
        if check_ollama_running(ollama_host):
            print_success("Ollama server is running")
            return True
        time.sleep(2)
    print_warning("Ollama server not responding")
    return False


def ensure_layout(paths: InstallPaths) -> bool:
    print_step("Creating standard GuardRag directory layout")
    try:
        for directory in [paths.install_root, paths.docs_dir, paths.data_dir, paths.logs_dir, paths.config_dir, paths.ollama_models_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        print_success(f"Install root ready at {paths.install_root}")
        return True
    except OSError as err:
        print_error(f"Failed to create directory structure: {err}")
        return False


def create_virtualenv(paths: InstallPaths) -> bool:
    print_step(f"Setting up virtual environment at {paths.venv_dir}")
    if paths.venv_dir.exists():
        print_warning("Virtual environment already exists, reusing it")
        return True
    try:
        subprocess.run([sys.executable, "-m", "venv", str(paths.venv_dir)], check=True)
        print_success("Virtual environment created")
        return True
    except subprocess.CalledProcessError as err:
        print_error(f"Failed to create virtual environment: {err}")
        return False


def get_venv_python(paths: InstallPaths) -> Path:
    if platform.system() == "Windows":
        return paths.venv_dir / "Scripts" / "python.exe"
    return paths.venv_dir / "bin" / "python"


def get_venv_pip(paths: InstallPaths) -> Path:
    if platform.system() == "Windows":
        return paths.venv_dir / "Scripts" / "pip.exe"
    return paths.venv_dir / "bin" / "pip"


def install_dependencies(paths: InstallPaths) -> bool:
    print_step("Installing Python dependencies")
    pip_path = get_venv_pip(paths)
    python_path = get_venv_python(paths)
    if not pip_path.exists():
        print_error(f"pip not found at {pip_path}")
        return False
    if not python_path.exists():
        print_error(f"python not found at {python_path}")
        return False
    if not paths.requirements_file.exists():
        print_error(f"requirements file not found at {paths.requirements_file}")
        return False

    try:
        subprocess.run([str(python_path), "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([str(python_path), "-m", "pip", "install", "-r", str(paths.requirements_file)], check=True)
        print_success(f"Dependencies installed from {paths.requirements_file}")
        return True
    except subprocess.CalledProcessError as err:
        print_error(f"Failed to install dependencies: {err}")
        return False


def setup_environment(paths: InstallPaths) -> bool:
    print_step("Setting up environment configuration")
    if paths.env_file.exists():
        print_warning(f"{paths.env_file.name} already exists, keeping it")
        return True

    if paths.env_example.exists():
        shutil.copy(paths.env_example, paths.env_file)
    else:
        paths.env_file.write_text("OLLAMA_HOST=http://localhost:11434\n", encoding="utf-8")

    # Installer metadata helps troubleshoot user setups.
    install_meta = paths.config_dir / "install.info"
    install_meta.write_text(
        f"install_root={paths.install_root}\nproject_root={PROJECT_ROOT}\n",
        encoding="utf-8",
    )
    print_success(f"Configured environment at {paths.env_file}")
    return True


def pull_ollama_model(ollama_cmd: Path, model_name: str, paths: InstallPaths) -> bool:
    print_step(f"Pulling Ollama model '{model_name}'")
    env = os.environ.copy()
    env["OLLAMA_MODELS"] = str(paths.ollama_models_dir)

    try:
        process = subprocess.Popen(
            [str(ollama_cmd), "pull", model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
        )
        assert process.stdout is not None
        for line in process.stdout:
            text = line.strip()
            if text:
                print(f"   {text}")
        rc = process.wait()
        if rc == 0:
            print_success(f"Model {model_name} pulled successfully")
            return True
    except OSError as err:
        print_error(f"Failed to run ollama pull: {err}")
        return False

    print_warning(f"Model pull failed for {model_name}. You can retry after setup.")
    return False


def validate_installation(paths: InstallPaths) -> bool:
    print_step("Validating installation")
    python_path = get_venv_python(paths)
    imports_to_check = [
        ("fastapi", "FastAPI"),
        ("haystack", "Haystack"),
        ("sentence_transformers", "SentenceTransformers"),
    ]
    all_ok = True
    for module, label in imports_to_check:
        result = subprocess.run([str(python_path), "-c", f"import {module}"], capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"{label} import OK")
        else:
            print_warning(f"{label} import failed")
            all_ok = False
    return all_ok


def launch_app(paths: InstallPaths) -> bool:
    print_step("Launching GuardRag GUI")
    python_path = get_venv_python(paths)
    if not paths.app_entrypoint.exists():
        print_warning(f"App entrypoint not found: {paths.app_entrypoint}")
        return False

    kwargs: dict[str, object] = {"cwd": str(PROJECT_ROOT)}
    if platform.system() == "Windows":
        kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE
    try:
        subprocess.Popen([str(python_path), str(paths.app_entrypoint)], **kwargs)
        print_success("GuardRag launched")
        return True
    except OSError as err:
        print_warning(f"Could not launch GuardRag automatically: {err}")
        return False


def print_banner() -> None:
    print(
        f"\n{Colors.BOLD}======================================\n"
        f"        GuardRag Installer v1.1       \n"
        f"======================================{Colors.RESET}\n"
    )


def print_next_steps(paths: InstallPaths, ollama_installed: bool, ollama_running: bool, model_name: str) -> None:
    print(f"\n{Colors.BOLD}{'=' * 50}\nNext Steps\n{'=' * 50}{Colors.RESET}\n")
    step = 1
    if not ollama_installed:
        print(f"{step}. Install Ollama from https://ollama.com/download")
        step += 1
    if not ollama_running:
        print(f"{step}. Start Ollama with: ollama serve")
        step += 1
    print(f"{step}. Activate the virtual environment:")
    if platform.system() == "Windows":
        print(f"   {paths.venv_dir}\\Scripts\\activate")
    else:
        print(f"   source {paths.venv_dir}/bin/activate")
    step += 1
    print(f"{step}. Pull model if needed: ollama pull {model_name}")
    step += 1
    print(f"{step}. Run the GUI app: python pipelines/rag_pipeline.py")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GuardRag installer")
    parser.add_argument("--skip-models", action="store_true", help="Skip pulling Ollama model")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model to pull (default: {DEFAULT_MODEL})")
    parser.add_argument(
        "--install-root",
        default=str(PROJECT_ROOT),
        help="Target installation root for venv/runtime directories",
    )
    parser.add_argument(
        "--ollama-host",
        default=DEFAULT_OLLAMA_HOST,
        help=f"Ollama host URL (default: {DEFAULT_OLLAMA_HOST})",
    )
    parser.add_argument(
        "--wait-ollama-seconds",
        type=int,
        default=20,
        help="Seconds to wait for Ollama service before skipping model pull",
    )
    parser.add_argument("--launch-app", action="store_true", help="Launch GuardRag GUI after install")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print_banner()
    if not check_python_version():
        return 1

    paths = build_paths(Path(args.install_root).resolve())
    ollama_cmd = check_ollama_installed()
    ollama_running = False
    if ollama_cmd:
        ollama_running = wait_for_ollama(args.ollama_host, args.wait_ollama_seconds)

    if not ensure_layout(paths):
        return 1
    if not create_virtualenv(paths):
        return 1
    if not install_dependencies(paths):
        return 1
    if not setup_environment(paths):
        return 1

    if not args.skip_models and ollama_cmd and ollama_running:
        pull_ollama_model(ollama_cmd, args.model, paths)
    elif not args.skip_models:
        print_warning("Skipping model pull because Ollama is missing or not running")

    validate_installation(paths)
    if args.launch_app:
        launch_app(paths)

    print_next_steps(paths, ollama_cmd is not None, ollama_running, args.model)
    print(f"\n{Colors.GREEN}{Colors.BOLD}Installation complete!{Colors.RESET}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
