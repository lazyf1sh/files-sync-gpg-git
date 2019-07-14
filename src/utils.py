import hashlib
import io
import json
import os
import sys
import shlex
import subprocess
import time

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
    """

    :rtype: object
    """
    if not os.path.exists(catalog_path):
        try:
            print("creating dir: ", catalog_path)
            os.makedirs(catalog_path)
            print("dir created: ", catalog_path)
            return True
        except FileExistsError as e:
            print(e)
            return False
    else:
        print(catalog_path + " is alread exists.")
        return False


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


def execute_command_args_bytes(args, working_dir):
    return execute_command_internal(args, working_dir)


def execute_command_internal(args, working_dir):
    """

    :param args:
    :param working_dir:
    :return: bytes
    """
    previous_working_dir = os.getcwd()
    os.chdir(working_dir)
    try:
        proc = subprocess.check_output(args)
        print("Output: \n{}\n".format(proc))
        return proc
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)
        raise CommandExecutionException
    finally:
        os.chdir(previous_working_dir)


def execute_command_args(args, working_dir) -> str:
    bytes1 = execute_command_internal(args, working_dir)
    try:
        return bytes1.decode("UTF-8")
    except Exception as e:
        print(e)
        return str(bytes1)


def execute_command_string(command, working_dir) -> str:
    args = shlex.split(command, posix="win" not in sys.platform)
    bytes1 = execute_command_internal(args, working_dir)
    try:
        return bytes1.decode("UTF-8")
    except Exception as e:
        print(e)
        return str(bytes1)


def get_current_unix_ts():
    return str(time.time()).split('.')[0]


def write_bytes_to_file(byte_arr, output_path):
    f = open(output_path, 'wb')
    f.write(byte_arr)
    f.close()


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        i = iter(lambda: f.read(4096), b"")
        for chunk in i:
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def md5_from_bytes(bytes):
    f = io.BytesIO(bytes)
    hash_md5 = hashlib.md5()

    i = iter(lambda: f.read(4096), b"")
    for chunk in i:
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def md5_from_string(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()
