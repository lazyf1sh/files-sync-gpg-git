import json
import os
import sys
import shlex
import subprocess


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


def create_dirs(dir):
    if not os.path.exists(dir):
        try:
            print("creating dir: ", dir)
            os.makedirs(dir)
            print("dir created: ", dir)
            return True
        except FileExistsError as e:
            print(e)


def buildAbsolutePath(relPath, srcFolder):
    srcFolder = srcFolder.replace("*", "")
    return srcFolder + "/" + relPath


def create_enc_dir_structure(files_enencrypted, src_folder, target_folder):
    for relPath in files_enencrypted:
        absPath = buildAbsolutePath(relPath, src_folder)
        if os.path.isdir(absPath):
            absPathOutput = buildAbsolutePath(relPath, target_folder)
            if absPathOutput.find(".") == 0:
                continue
            else:
                if not os.path.exists(absPathOutput):
                    os.makedirs(absPathOutput)


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
        return
    else:
        print("Output: \n{}\n".format(proc))
    return format(proc)
