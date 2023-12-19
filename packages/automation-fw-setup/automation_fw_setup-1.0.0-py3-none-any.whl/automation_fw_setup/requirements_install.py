import subprocess
import os
from colorama import Fore, Style

def install_requirements(project_name):
    print(f"{Fore.YELLOW}!{Style.RESET_ALL} Installing requirements on virtual env (venv)...")
    python_path = f"{project_name}/venv/Scripts/python" if os.name == 'nt' else f"./{project_name}/venv/bin/python"
    try:
        subprocess.run([python_path, "-m", "pip", "install", "-r", f"{project_name}/requirements.txt"], check=True)
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}✗{Style.RESET_ALL} Failed to install requirements.")
        return
    except subprocess.SubprocessError:
        print(f"{Fore.RED}✗{Style.RESET_ALL} An error occurred while installing the requirements.")
        return

    print(f"{Fore.YELLOW}!{Style.RESET_ALL} Finalizing Browser library installation with rfbrowser init...")
    rfbrowser_path = f"{project_name}/venv/Scripts/rfbrowser" if os.name == 'nt' else f"./{project_name}/venv/bin/rfbrowser"
    try:
        subprocess.run([rfbrowser_path, "init"], check=True)
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}✗{Style.RESET_ALL} Failed to initialize Browser library.")
        return
    except subprocess.SubprocessError:
        print(f"{Fore.RED}✗{Style.RESET_ALL} An error occurred while initializing the Browser library.")
        return