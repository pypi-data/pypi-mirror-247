import os
from colorama import Fore, Style

def create_project_folder():
    while True:
        project_name = input("Please enter the project name: ")
        if os.path.exists(project_name):
            print(f"{Fore.RED}✗{Style.RESET_ALL} A folder with this name already exists. Please provide a new name.")
        else:
            os.mkdir(project_name)
            return project_name