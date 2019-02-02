import subprocess
import os

recipient = "94B31905EEA476BA62B105D0BBDC9AD25A5BEF95!"





def encrypt_files(list_files, src_folder, target_folder):
    for relPath in list_files:
        absPath = src_folder.replace("*", "") + relPath
        if os.path.isfile(absPath) and not absPath.lower().endswith('.gpg'):
            path_encrypted = target_folder + relPath
            print(subprocess.check_output(['gpg', '--yes', '--verbose', '--output', path_encrypted + '.gpg', '--encrypt', '--recipient', recipient, absPath]))
