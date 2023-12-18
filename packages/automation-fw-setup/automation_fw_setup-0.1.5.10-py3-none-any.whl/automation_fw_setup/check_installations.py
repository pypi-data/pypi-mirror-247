import subprocess
import sys
import inquirer
from colorama import Fore, Style

def install_robot_framework():
    print("Installing Robot Framework...")
    subprocess.run(["venv/bin/python", "-m", "pip", "install", "robotframework"], check=True)

def check_installation(program_name, check_command, install_function=None):
    check_command = check_command.split()  # split the command into a list
    result = subprocess.run(check_command, capture_output=True, text=True)
    output = result.stdout.strip() if result.stdout.strip() else result.stderr.strip()
    if result.returncode != 0:
        print(f"{Fore.RED}✗{Style.RESET_ALL} Could not detect {program_name} version")
        if install_function:
            questions = [
                inquirer.Confirm('install',
                                 message=f"Do you want to install {program_name}?"),
            ]
            answers = inquirer.prompt(questions)
            if answers['install']:
                install_function()
                return True
        return False
    else:
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} {program_name} version detected: {output}")
        return True

def check_installations():
    programs = [
        {"name": "Python", "command": "python --version"},
        {"name": "pip", "command": "pip --version"},
        {"name": "Robot Framework", "command": "robot --version", "install": install_robot_framework},
        {"name": "Node.js", "command": "node --version", "install_url": "https://nodejs.org/en/download/"},
    ]

    for program in programs:
        check_installation(program["name"], program["command"], program.get("install"))