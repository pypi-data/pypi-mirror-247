import sys
import os
import pkg_resources

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from automation_fw_setup.check_installations import check_installations
from automation_fw_setup.create_project_folder import create_project_folder
from automation_fw_setup.create_virtual_env import create_virtual_env
from automation_fw_setup.ask_test_framework import ask_test_framework
from automation_fw_setup.ask_target_platform import ask_target_platform
from automation_fw_setup.clone_repository import clone_repository
from automation_fw_setup.requirements_install import install_requirements
from colorama import Fore, Style

def main():

    # Get the current version
    try:
        current_version = pkg_resources.get_distribution('automation-fw-setup').version
    except pkg_resources.DistributionNotFound:
        current_version = 'local'

    print(f"Creating your awesome project using Automation Framework Setup v{current_version}")

    framework_choice = ask_test_framework()

    if framework_choice == 'Robot Framework':
        platform_choice = ask_target_platform()
        if platform_choice == 'Web':
            project_name = create_project_folder()
            clone_repository(project_name)
            create_virtual_env(project_name)
            check_installations(project_name)
            install_requirements(project_name)
        else:
            print(f"{Fore.RED}✗{Style.RESET_ALL} The selected platform is not yet supported.")

if __name__ == "__main__":
    main()