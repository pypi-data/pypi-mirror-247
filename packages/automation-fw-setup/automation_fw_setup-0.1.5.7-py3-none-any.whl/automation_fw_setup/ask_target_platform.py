import inquirer
from colorama import Fore, Style

def ask_target_platform():
    questions = [
        inquirer.List('platform',
                      message="Please select the target platform for automation",
                      choices=['Web', 'Mobile', 'Desktop', 'Mainframe'],
                      ),
    ]
    answers = inquirer.prompt(questions)
    return answers['platform']