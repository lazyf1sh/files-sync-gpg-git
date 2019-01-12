import glob
import os
import subprocess
import time

def decrypt_run(folder_encrypted, folder_unencrypted):
    files = glob.glob(folder_encrypted + "**", recursive=True)
    for file in files:
        if os.path.isfile(file) and file.lower().endswith('.gpg'):
            rel_file = os.path.relpath(file, folder_encrypted)
            rel_file = folder_unencrypted.replace("**", "") + "decrypted-to-merge-" + str(int(time.time())) + "/" + rel_file
            print(subprocess.check_output(['gpg', '--yes', '--output', file.replace('.gpg', ''), '--verbose', '--decrypt', file]))
