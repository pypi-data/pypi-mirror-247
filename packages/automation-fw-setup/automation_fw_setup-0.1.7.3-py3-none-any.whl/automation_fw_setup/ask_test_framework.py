import inquirer
from colorama import Fore, Style

def ask_test_framework():
    questions = [
        inquirer.List('framework',
                      message="Please select the test framework to be used",
                      choices=['Robot Framework', 'Playwright', 'Cypress'],
                      ),
    ]
    answers = inquirer.prompt(questions)
    return answers['framework']