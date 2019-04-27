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


def decrypt_single_file(source_path, target_path):
    if os.path.isfile(source_path):
        output = subprocess.check_output(['gpg', '--yes', '--output', target_path, '--verbose', '--decrypt', source_path])
        print(output)


def decrypt_single_file_inmemory(source_path):
    """
    :rtype: str
    :param source_path: source file path
    :return: file contents
    """
    if os.path.isfile(source_path):
        output = subprocess.check_output(['gpg', '--yes', '--verbose', '--decrypt', source_path])
        return output