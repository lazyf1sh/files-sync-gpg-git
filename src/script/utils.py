import hashlib
import io
import json
import logging
import ntpath
import os
import shlex
import shutil
import subprocess
import sys
import time


logger = logging.getLogger(__name__)


def stop_application(locked_file, lock_file_path):
    locked_file.close()
    os.remove(lock_file_path)
    logger.info("called stop_application")
    sys.exit(0)


def read_json_dict_from_file(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
        return data


def dict_to_json(filename, my_dict):
    with open(filename, 'w') as file:
        json.dump(my_dict, file, indent=4, sort_keys=True)


def remove_dirs(dir_path):
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        if not os.listdir(dir_path):
            shutil.rmtree(dir_path)
        else:
            logger.critical("Directory is not empty: %s", dir_path)
            raise Exception("Dir is not empty")
    else:
        logger.info("Given Directory don't exists: %s", dir_path)


def create_dirs(catalog_path):
    """

    :rtype: object
    """
    if not os.path.exists(catalog_path):
        try:
            logger.debug("creating dir: ", catalog_path)
            os.makedirs(catalog_path)
            logger.debug("dir created: ", catalog_path)
            return True
        except FileExistsError as e:
            logger.info(e)
            return False
    else:
        logger.debug("Catalog already exists: %s", catalog_path)
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


def calc_path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def calc_path_head(path):
    head, tail = ntpath.split(path)
    return head


def append_ts_to_path(path, current_ts):
    leaf = calc_path_leaf(path)
    head = calc_path_head(path)
    return head + "/" + current_ts + "_" + leaf


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
    logging.debug("executing command: %s", args)
    previous_working_dir = os.getcwd()
    os.chdir(working_dir)
    try:
        proc = subprocess.check_output(args)
        # logger.debug("Command executed: %s\nExec result: %s\n", args, proc)
        return proc
    except subprocess.CalledProcessError as exc:
        logger.critical("Critical error. Code: %s \n\n Output: %s", exc.returncode, exc.output)
        raise exc
    finally:
        os.chdir(previous_working_dir)


def execute_command_args(args, working_dir) -> str:
    my_bytes = execute_command_internal(args, working_dir)
    try:
        return my_bytes.decode("UTF-8")
    except Exception as e:
        logger.warning(e)
        return str(my_bytes)


def execute_command_string(command, working_dir) -> str:
    args = shlex.split(command, posix="win" not in sys.platform)
    bytes1 = execute_command_internal(args, working_dir)
    try:
        return bytes1.decode("UTF-8")
    except Exception as e:
        logger.critical(e)
        raise Exception("Error executing command")


def get_current_unix_ts():
    return str(time.time()).split('.')[0]


def write_bytes_to_file(byte_arr, output_path):
    f = open(output_path, 'wb')
    f.write(byte_arr)
    f.close()


def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        i = iter(lambda: f.read(4096), b"")
        for chunk in i:
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def md5_from_bytes(my_bytes):
    f = io.BytesIO(my_bytes)
    hash_md5 = hashlib.md5()

    i = iter(lambda: f.read(4096), b"")
    for chunk in i:
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def md5_from_string(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()
