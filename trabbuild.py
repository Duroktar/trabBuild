from __future__ import print_function
import os
import re
import sys
import subprocess
import yaml
from distutils.version import LooseVersion


SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))

VERSION_REGEX = re.compile(r"(?:(\d+\.(?:\d+\.)*\d+))", re.S)

VERSION = None
OLD_SETUP = None
CONFIG_FILE = 'trabconfig.yml'

def get_config():
    if not os.path.isfile(CONFIG_FILE):
        CONFIG_FILE = os.path.join(SCRIPT_PATH, CONFIG_FILE)
    with open(CONFIG_FILE, 'r') as f:
        return yaml.load(f.read())


def write_setup_file(lines):
    with open('setup.py', 'w') as f:
        f.writelines(lines)


def read_setup_file():
    with open('setup.py', 'r+') as f:
        return f.readlines()


def get_current_version(line):
    """Returns the current version of the module"""
    current_version = re.search(VERSION_REGEX, line).group()
    print("Current version:", current_version)
    global VERSION
    VERSION = current_version
    return current_version


def get_new_version(current_version):
    new_version = raw_input("Enter new version or `q` to exit - $ ")
    if new_version == 'q':
        sys.exit()
    if LooseVersion(new_version) > LooseVersion(current_version):
        return new_version
    else:
        print("Not a valid version number. \n"
              "Please select a version higher than the current one..")
        get_new_version(current_version)


def update_version(new_version, version_line):
    return re.sub(VERSION_REGEX, new_version, version_line)


def migrate_version():
    setup_file = read_setup_file()
    global OLD_SETUP
    OLD_SETUP = setup_file
    for index, line in enumerate(setup_file):
        if line.startswith("__version__ ="):
            current_version = get_current_version(line)
            new_version = get_new_version(current_version)
            new_line = update_version(new_version, line)
            setup_file[index] = new_line
            return write_setup_file(setup_file)


def make_builds(config_):
    confirm = raw_input("Build distros?  [y] or n ") or 'y'
    if not confirm == 'y':
        print("Aborting.")
        return
    commands = config_['Commands']
    twine = config_['Twine']
    for cmd in commands:
        try:
            subprocess.call(cmd, shell=True)
        except Exception as e:
            print("Error processing", str(cmd))
            print(e)

    confirm = raw_input("Do you want to upload to twine?  y [n] ") or 'n'
    if confirm == 'n':
        return
    response = subprocess.call(twine, shell=True)
    if response == 127:
        print("Twine not installed.. Aborting.")


def get_module_name():
    setup = read_setup_file()
    for line in setup:
        line = line.strip()
        if line.startswith("name=") or line.startswith("name ="):
            name = re.search(r'[\"\'](.+)[\"\']', line).group()
            return name.strip('"').strip("'")
    print("Couldn't find the name of the module!")
    sys.exit()


def main():
    if not os.path.isfile('setup.py'):
        print("No setup.py file found! Aborting..")
        sys.exit()

    module_name = get_module_name()
    print("Welcome to trabBuild!")
    print("Ready to update and build package ~ %s ~" % module_name)

    proceed = raw_input("Continue?  [y] or n $ ") or 'y'
    if proceed.lower() not in ['y', 'n']:
        main()
    elif not proceed.lower() == 'y':
        print("Goodbye!")
        sys.exit()

    migrate_version()
    try:
        config = get_config()
        make_builds(config)
    except Exception as e:
        print("There was an exception -", e)

        c = raw_input("Would you like to revert back to version %s?  [y] or n" % VERSION) or 'y'
        if c == 'y':
            write_setup_file(OLD_SETUP)
        print("Goodbye!")


if __name__ == "__main__":
    main()
