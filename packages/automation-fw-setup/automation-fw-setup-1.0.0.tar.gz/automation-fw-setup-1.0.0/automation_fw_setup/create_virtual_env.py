import os
import subprocess
from colorama import Fore, Style

def create_virtual_env(project_name):
    venv_dir = os.path.join(project_name, 'venv')
    try:
        subprocess.run(['python', '-m', 'venv', venv_dir], check=True)
    except subprocess.CalledProcessError:
        print("Failed to create virtual environment with python. Trying with python3...")
        try:
            subprocess.run(['python3', '-m', 'venv', venv_dir], check=True)
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}✗{Style.RESET_ALL} Failed to create virtual environment with python3.")
            return
    except subprocess.SubprocessError:
        print(f"{Fore.RED}✗{Style.RESET_ALL} An error occurred while creating the virtual environment.")
        return

    print(f"{Fore.GREEN}✓{Style.RESET_ALL} Virtual environment created successfully.")
    print(f"{Fore.YELLOW}!{Style.RESET_ALL} To activate the virtual environment, navigate to the project directory and use the following command:")
    print(f"On Linux/macOS: source {os.path.join(venv_dir, 'bin', 'activate')}")
    print(f"On Windows: .\\{os.path.join(venv_dir, 'Scripts', 'activate')}")