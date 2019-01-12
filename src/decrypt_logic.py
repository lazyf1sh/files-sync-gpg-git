import glob
import os
import subprocess


def decrypt_run(folder_encrypted, folder_unencrypted):
    files = glob.glob(folder_encrypted + "**", recursive=True)
    for file in files:
        if os.path.isfile(file) and file.lower().endswith('.gpg'):
            print(subprocess.check_output(['gpg', '--yes', '--output', file.replace('.gpg', ''), '--verbose', '--decrypt', file]))
