import subprocess
from colorama import Fore, Style

def install_requirements(project_name):
    print(f"{Fore.YELLOW}!{Style.RESET_ALL} Installing requirements on virtual env (venv)...")
    subprocess.run([f"./{project_name}/venv/bin/python", "-m", "pip", "install", "-r", f"{project_name}/requirements.txt"], check=True)
    print(f"{Fore.YELLOW}!{Style.RESET_ALL} Finalizing Browser library installation with rfbrowser init...")
    subprocess.run([f"./{project_name}/venv/bin/rfbrowser", "init"], check=True)