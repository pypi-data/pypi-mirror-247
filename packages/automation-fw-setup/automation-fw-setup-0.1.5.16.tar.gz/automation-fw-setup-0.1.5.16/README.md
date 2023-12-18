# Test Automation Project Setup

This project is a script to set up a new test automation project. It asks the user to select a test framework and a target platform for automation.

## Current Version

The current version of the program is 0.1.5.14.

## Installation

You can install the Test Automation Project Setup using pip:

```sh
pip install automation-fw-setup
```

## Usage

After installation, you can run the program using the following command:

```sh
automation_fw_setup
```

This will start the program, which will guide you through the process of setting up your test automation project.

Alternatively, you can run the `main.py` script:

```sh
python main.py
```

The script will ask you to select a test framework and a target platform for automation.

Currently, the only supported test framework is 'Robot Framework' and the only supported target platform is 'Web'. If you select any other options, the script will inform you that the selected option is not yet supported and will terminate.

## Future Enhancements

Support for 'Playwright' and 'Cypress' test frameworks, and 'Mobile', 'Desktop', and 'Mainframe' target platforms will be added in the future.

## Contributions

Contributions to this project are welcome! If you have a feature request, bug report, or proposal, please open an issue. If you wish to contribute code, please open a pull request.