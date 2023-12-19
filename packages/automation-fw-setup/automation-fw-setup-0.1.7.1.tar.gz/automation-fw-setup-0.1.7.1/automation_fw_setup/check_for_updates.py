# check_for_updates.py

import pkg_resources
import subprocess
import sys

def check_for_updates():
    # Get the current version of the package
    try:
        current_version = pkg_resources.get_distribution('automation-fw-setup').version
    except pkg_resources.DistributionNotFound:
        current_version = 'local'
    # Get the latest version available on PyPI
    result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', '--no-deps', '--no-install', 'automation-fw-setup'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    lines = result.stdout.decode('utf-8').split('\n')
    latest_version = next((line.split(' ')[1] for line in lines if 'Collecting' in line), current_version)

    # Check if the current version is the latest version
    if current_version != latest_version:
        print(f"A new version of automation-fw-setup is available: {latest_version}. You are currently using version {current_version}. To upgrade, run: pip install --upgrade automation-fw-setup")