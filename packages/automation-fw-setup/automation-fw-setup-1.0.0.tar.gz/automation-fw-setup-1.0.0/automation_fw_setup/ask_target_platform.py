import inquirer
import sys  # new import
from colorama import Fore, Style

def ask_target_platform():
    questions = [
        inquirer.List('platform',
                      message="Please select the target platform for automation",
                      choices=['Web', 'Mobile', 'Desktop', 'Mainframe'],
                      ),
    ]

    answers = inquirer.prompt(questions)

    if answers is None:
        print("\nSelection cancelled by user. Exiting...")
        sys.exit(0)

    return answers['platform']