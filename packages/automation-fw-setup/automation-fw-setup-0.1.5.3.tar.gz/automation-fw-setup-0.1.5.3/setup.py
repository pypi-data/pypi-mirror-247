from setuptools import setup, find_packages

# Find packages
packages = find_packages()

# Print packages
print("Packages:", packages)

setup(
    name='automation-fw-setup',
    version='0.1.5.3',
    url='https://github.com/cccarv82/autotool',
    author='Carlos Carvalho',
    author_email='cccarv82@gmail.com',
    description='A tool for setting up a test automation project with various frameworks and platforms.',
    packages=packages,    
    install_requires=['gitpython', 'colorama', 'inquirer'],
    entry_points={
        'console_scripts': [
            'automation_fw_setup=automation_fw_setup.__main__:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)