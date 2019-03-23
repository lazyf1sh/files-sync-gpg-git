import json
import os
import sys
import shlex
import subprocess

from src import CommandExecutionException


def stop_application():
    print("called stop_application\n")
    sys.exit(0)


def read_json_dict_from_file(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
        return data


def dict_to_json(filename, my_dict):
    with open(filename, 'w') as file:
        json.dump(my_dict, file, indent=4, sort_keys=True)


def create_dirs(catalog_path):
    if not os.path.exists(catalog_path):
        try:
            print("creating dir: ", catalog_path)
            os.makedirs(catalog_path)
            print("dir created: ", catalog_path)
            return True
        except FileExistsError as e:
            print(e)


def build_absolute_path(rel_path, folder_path):
    folder_path = folder_path.replace("*", "")
    return folder_path + "/" + rel_path


def create_enc_dir_structure(files_enencrypted, src_folder, target_folder):
    for rel_path in files_enencrypted:
        abs_path = build_absolute_path(rel_path, src_folder)
        if os.path.isdir(abs_path):
            abs_output_path = build_absolute_path(rel_path, target_folder)
            if abs_output_path.find(".") == 0:
                continue
            else:
                if not os.path.exists(abs_output_path):
                    os.makedirs(abs_output_path)


def remove_files(paths, src_folder, target_folder):
    for relPath in paths:
        src_folder = src_folder.replace("**", "")
        encrypted_path = target_folder + relPath + ".gpg"
        if os.path.exists(encrypted_path) and os.path.isfile(encrypted_path):
            os.remove(encrypted_path)


def execute_command(command):
    args = shlex.split(command)
    try:
        proc = subprocess.check_output(args)
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)
        raise CommandExecutionException
    else:
        print("Output: \n{}\n".format(proc))
