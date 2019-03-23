import configparser
import subprocess
import os

config = configparser.ConfigParser()
config.read('default.conf')

recipient = config["default"]["gpg-recipient"]


def encrypt_files(list_files, src_folder, target_folder):
    for relPath in list_files:
        abs_path = src_folder.replace("*", "") + relPath
        if os.path.isfile(abs_path) and not abs_path.lower().endswith('.gpg'):
            path_encrypted = target_folder + relPath
            print(subprocess.check_output(['gpg', '--yes', '--verbose', '--output', path_encrypted + '.gpg', '--encrypt', '--recipient', recipient, abs_path]))
