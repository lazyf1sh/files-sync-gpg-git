import configparser
import subprocess
import os

config = configparser.ConfigParser()
config.read('default.conf')

recipient = config["default"]["gpg-recipient"]

# deprecated
def encrypt_files(list_files, src_folder, target_folder):
    for relPath in list_files:
        abs_path = src_folder.replace("*", "") + relPath


def encrypt_single_file(src_path, target_path):
    if os.path.isfile(src_path):
        print(subprocess.check_output(['gpg', '--yes', '--verbose', '--output', target_path, '--encrypt', '--recipient', recipient, src_path]))
    else:
        print(src_path + "is not a file")
