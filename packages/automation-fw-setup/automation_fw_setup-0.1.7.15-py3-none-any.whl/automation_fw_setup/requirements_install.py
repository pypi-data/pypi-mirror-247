import subprocess
import os
from colorama import Fore, Style

def install_requirements(project_name):
    print(f"{Fore.YELLOW}!{Style.RESET_ALL} Installing requirements on virtual env (venv)...")
    python_path = f"{project_name}/venv/Scripts/python" if os.name == 'nt' else f"./{project_name}/venv/bin/python"
    subprocess.run([python_path, "-m", "pip", "install", "-r", f"{project_name}/requirements.txt"], check=True)
    print(f"{Fore.YELLOW}!{Style.RESET_ALL} Finalizing Browser library installation with rfbrowser init...")
    rfbrowser_path = f"{project_name}/venv/Scripts/rfbrowser" if os.name == 'nt' else f"./{project_name}/venv/bin/rfbrowser"
    subprocess.run([rfbrowser_path, "init"], check=True)