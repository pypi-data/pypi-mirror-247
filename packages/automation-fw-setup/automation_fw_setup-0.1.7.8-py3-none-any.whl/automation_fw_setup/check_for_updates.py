# check_for_updates.py

import pkg_resources
import subprocess
import sys

import requests

from colorama import Fore, Style

def check_for_updates():
    # Get the current version of the package
    try:
        current_version = pkg_resources.get_distribution('automation-fw-setup').version
    except pkg_resources.DistributionNotFound:
        current_version = 'local'

    # Skip update check for local development version
    if current_version == 'local':
        return

    # Get the latest version available on PyPI
    response = requests.get('https://pypi.org/pypi/automation-fw-setup/json')
    releases = response.json()['releases']
    latest_version = sorted(releases.keys(), key=pkg_resources.parse_version, reverse=True)[0]

    # Check if the current version is the latest version
    from colorama import Fore, Style

    if current_version != latest_version:
        print(f"{Fore.RED}✗{Style.RESET_ALL} {Style.BRIGHT}A new version of automation-fw-setup is available: {Fore.GREEN}{latest_version}{Style.RESET_ALL}. You are currently using version {Fore.RED}{current_version}{Style.RESET_ALL}. To upgrade, run: pip install --upgrade automation-fw-setup{Style.RESET_ALL}")
        sys.exit(1)  # Exit the program