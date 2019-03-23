import glob
import os
import subprocess


def decrypt_run(folder_encrypted, folder_unencrypted):
    decrypt_dir = folder_unencrypted.replace("**", "") # + "!decrypted-to-merge-" + str(int(time.time())) + "/"
    files = glob.glob(folder_encrypted + "/**", recursive=True)
    for file in files:
        if os.path.isfile(file) and file.lower().endswith('.gpg'):
            rel_file = decrypt_dir + os.path.relpath(file, folder_encrypted)
            print(subprocess.check_output(['gpg', '--yes', '--output', rel_file.replace('.gpg', ''), '--verbose', '--decrypt', file]))
