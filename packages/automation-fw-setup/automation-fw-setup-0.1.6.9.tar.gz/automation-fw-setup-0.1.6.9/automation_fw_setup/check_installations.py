import platform
import subprocess
import sys
import inquirer
from colorama import Fore, Style
import os

def install_robot_framework(project_name):
    print("Installing Robot Framework...")
    python_path = f"{project_name}/venv/bin/python" if os.name != 'nt' else f"{project_name}\\venv\\Scripts\\python"
    subprocess.run([python_path, "-m", "pip", "install", "robotframework"], check=True)

def check_installation(program_name, check_command, project_name, install_function=None):
    if program_name == "Python":
        version = platform.python_version()
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} {program_name} version detected: {version}")
        return True
    else:
        check_command = check_command.split()  # split the command into a list
        venv_activate = os.path.join(project_name, 'venv', 'Scripts', 'activate') if os.name == 'nt' else f"source {project_name}/venv/bin/activate"
        check_command = f"{venv_activate} && {' '.join(check_command)}"
        result = subprocess.run(check_command, capture_output=True, text=True, shell=True)
        output = result.stdout.strip() if result.stdout.strip() else result.stderr.strip()
        if result.returncode != 0:
            if install_function:
                questions = [
                    inquirer.Confirm('install',
                                     message=f"Do you want to install {program_name} in the Virtual Env ?"),
                ]
                answers = inquirer.prompt(questions)
                if answers['install']:
                    install_function(project_name)
                    return True
            return False
        else:
            print(f"{Fore.GREEN}✓{Style.RESET_ALL} {program_name} version detected: {output}")
            return True

def check_installations(project_name):
    python_path = f"{project_name}/venv/bin/python" if os.name != 'nt' else f"{project_name}\\venv\\Scripts\\python"
    programs = [
        {"name": "Python", "command": ""},
        {"name": "pip", "command": "pip --version"},
        {"name": "Robot Framework", "command": f"{python_path} -m robot --version", "install": install_robot_framework},
        {"name": "Node.js", "command": "node --version", "install_url": "https://nodejs.org/en/download/"},
    ]

    for program in programs:
        check_installation(program["name"], program["command"], project_name, program.get("install"))