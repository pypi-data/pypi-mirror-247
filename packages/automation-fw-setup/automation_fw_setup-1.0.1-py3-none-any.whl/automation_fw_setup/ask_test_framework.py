# ask_test_framework.py

import inquirer
import sys  # new import
from colorama import Fore, Style

def ask_test_framework():
    questions = [
        inquirer.List('framework',
                      message=f"{Fore.YELLOW}[?]{Style.RESET_ALL} Please select the test framework to be used:",
                      choices=['Robot Framework', 'Playwright', 'Cypress'],
                      ),
    ]

    answers = inquirer.prompt(questions)

    if answers is None:
        print("\nSelection cancelled by user. Exiting...")
        sys.exit(0)

    return answers['framework']