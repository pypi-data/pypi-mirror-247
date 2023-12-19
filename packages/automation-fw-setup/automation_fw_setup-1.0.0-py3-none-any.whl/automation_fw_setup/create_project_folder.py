import os
import re
from colorama import Fore, Style

def validate_project_name(project_name):
    if not project_name:
        print(f"{Fore.RED}✗{Style.RESET_ALL} Project name cannot be empty.")
        return False

    if len(project_name) > 255:
        print(f"{Fore.RED}✗{Style.RESET_ALL} Project name is too long.")
        return False

    if re.search(r'[<>:"/\\|?*]', project_name):
        print(f"{Fore.RED}✗{Style.RESET_ALL} Project name contains invalid characters.")
        return False

    if project_name in ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']:
        print(f"{Fore.RED}✗{Style.RESET_ALL} Project name is a reserved name.")
        return False

    return True

def create_project_folder():
    while True:
        project_name = input("Please enter the project name: ")
        if not validate_project_name(project_name):
            continue
        try:
            if os.path.exists(project_name):
                print(f"{Fore.RED}✗{Style.RESET_ALL} A folder with this name already exists. Please provide a new name.")
            else:
                try:
                    os.mkdir(project_name)
                    return project_name
                except OSError:
                    print(f"{Fore.RED}✗{Style.RESET_ALL} An error occurred while creating the project folder.")
        except OSError:
            print(f"{Fore.RED}✗{Style.RESET_ALL} An error occurred while checking if the project folder exists.")