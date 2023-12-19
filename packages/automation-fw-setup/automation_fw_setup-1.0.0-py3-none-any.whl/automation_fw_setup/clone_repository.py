import git
import os
import shutil
import subprocess
import platform
from colorama import Fore, Style

def clone_repository(project_name):
    repo_url = "https://github.com/cccarv82/rf-web-base-framework/"
    try:
        if os.listdir(project_name):
            print(f"{Fore.RED}✗{Style.RESET_ALL} The project directory is not empty. Please provide an empty directory for cloning the repository.")
            return
    except FileNotFoundError:
        print(f"{Fore.RED}✗{Style.RESET_ALL} The project directory does not exist.")
        return

    print(f"{Fore.YELLOW}!{Style.RESET_ALL} Cloning repository {repo_url} into the project directory...")
    try:
        git.Repo.clone_from(repo_url, project_name)
    except git.GitCommandError:
        print(f"{Fore.RED}✗{Style.RESET_ALL} An error occurred while cloning the repository.")
        return

    remove_git_dir(project_name)  # new line
    print(f"{Fore.GREEN}✓{Style.RESET_ALL} Repository cloned successfully.")
    print(f"{Fore.YELLOW}!{Style.RESET_ALL} Consider versioning your code using git. You can start by running the following commands in your project directory:")
    print("git init")
    print("git add .")
    print("git commit -m 'Initial commit'")
    print("For more information, visit: https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup")

def remove_git_dir(project_name):
    git_dir = os.path.join(project_name, '.git')
    if os.path.exists(git_dir):
        try:
            if platform.system() == 'Windows':
                subprocess.run(['rmdir', '/s', '/q', git_dir], shell=True)
            else:
                shutil.rmtree(git_dir, ignore_errors=True)
        except (subprocess.SubprocessError, OSError):
            print(f"{Fore.RED}✗{Style.RESET_ALL} An error occurred while removing the .git directory.")