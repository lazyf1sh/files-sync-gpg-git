import glob
import os
import subprocess


def decrypt_run(folder_encrypted, folder_unencrypted):
    decrypt_dir = folder_unencrypted.replace("**", "")  # + "!decrypted-to-merge-" + str(int(time.time())) + "/"
    files = glob.glob(folder_encrypted + "/**", recursive=True)
    for file in files:
        if os.path.isfile(file) and file.lower().endswith('.gpg'):
            rel_file = decrypt_dir + os.path.relpath(file, folder_encrypted)
            print(subprocess.check_output(['gpg', '--yes', '--output', rel_file.replace('.gpg', ''), '--verbose', '--decrypt', file]))


def decrypt_gpged_files(set_files, target_catalog_path, source_catalog_path):
    """
    Descrypts gpg-ed files to selected foler

    :param source_catalog_path:
    :param set_files: iterable to go over
    :param target_catalog_path: folder to decrypt
    """
    for file in set_files:
        source = source_catalog_path + file + ".gpg"
        target = target_catalog_path + file
        decrypt_single_file(source, target)


def decrypt_single_file(source_path, target_path):
    if os.path.isfile(source_path):
        try:
            output = subprocess.check_output(['gpg', '--yes', '--output', target_path, '--verbose', '--decrypt', source_path])
            print(output)
        except subprocess.CalledProcessError as e:
            print("error decrypting " + source_path + " " + str(e.output))
    else:
        print(source_path + " - is not a file")


def decrypt_single_file_inmemory_to_str(source_path):
    """
    :rtype: str
    :param source_path: source file path
    :return: file contents
    """
    if os.path.isfile(source_path):
        output = subprocess.check_output(['gpg', '--yes', '--verbose', '--decrypt', source_path])
        output = output.decode('UTF-8')
        return output

def decrypt_single_file_inmemory(source_path):
    """
    :rtype: str
    :param source_path: source file path
    :return: file contents
    """
    if os.path.isfile(source_path):
        output = subprocess.check_output(['gpg', '--yes', '--verbose', '--decrypt', source_path])
        return output