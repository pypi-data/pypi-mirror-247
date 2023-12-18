import os
import subprocess
import shutil
from colorama import Fore, Style

def create_virtual_env(project_name):
    python_executable = shutil.which('python')
    if python_executable is None:
        raise Exception("Could not find 'python' executable in PATH")
    venv_dir = os.path.join(project_name, 'venv')
    subprocess.run([python_executable, '-m', 'venv', venv_dir], check=True)
    print(f"{Fore.GREEN}✓{Style.RESET_ALL} Virtual environment created successfully.")
    print(f"{Fore.YELLOW}!{Style.RESET_ALL} To activate the virtual environment, navigate to the project directory and use the following command:")
    print(f"On Linux/macOS: source {os.path.join(venv_dir, 'bin', 'activate')}")
    print(f"On Windows: .\\{os.path.join(venv_dir, 'Scripts', 'activate')}")