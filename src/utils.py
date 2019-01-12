import json
import os
import sys


def stop_application():
    print("end\n")
    sys.exit(0)


def read_json_dict_from_file(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
        return data


def dict_to_json(filename, my_dict):
    with open(filename, 'w') as file:
        json.dump(my_dict, file, indent=4, sort_keys=True)


def create_target_dir(target_dir):
    if not os.path.exists(target_dir):
        try:
            os.makedirs(target_dir)
        except FileExistsError as e:
            print(e)


def create_enc_dir_structure(files_enencrypted, src_folder, target_folder):
    for file in files_enencrypted:
        if os.path.isdir(file):
            src_folder = src_folder.replace("**", "")
            path_encrypted = target_folder + os.path.relpath(file, src_folder)
            if path_encrypted.find(".") == 0:
                continue
            else:
                if not os.path.exists(path_encrypted):
                    os.makedirs(path_encrypted)


def remove_files(paths, src_folder, target_folder):
    for path in paths:
        src_folder = src_folder.replace("**", "")
        encrypted_path = target_folder + os.path.relpath(path, src_folder) + ".gpg"
        if os.path.exists(encrypted_path) and os.path.isfile(encrypted_path):
            os.remove(encrypted_path)
