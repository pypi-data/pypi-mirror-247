# check_for_updates.py

import pkg_resources
import subprocess
import sys

import requests

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
    if current_version != latest_version:
        print(f"A new version of automation-fw-setup is available: {latest_version}. You are currently using version {current_version}. To upgrade, run: pip install --upgrade automation-fw-setup")
        sys.exit(1)  # Exit the program