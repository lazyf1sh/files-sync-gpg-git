import hashlib
import io
import json
import logging
import ntpath
import os
import shutil
import sys
import time

logger = logging.getLogger(__name__)


def stop_script_no_args():
    logger.info("--------------- script finished ---------------")
    sys.exit(0)


def stop_script(locked_file, lock_file_path):
    locked_file.close()
    os.remove(lock_file_path)
    stop_script_no_args()


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
            logger.debug("creating dir: %s", catalog_path)
            os.makedirs(catalog_path)
            logger.debug("dir created: %s", catalog_path)
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


def calculate_conflicted_path(head, tail, current_ts):
    return head + "/" + "!" + current_ts + "_" + tail


def calc_path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def calc_path_head(path):
    head, tail = ntpath.split(path)
    return head


def append_ts_to_path(path, current_ts):
    leaf = calc_path_leaf(path)
    head = calc_path_head(path)
    return head + "/" + "!" + current_ts + "_" + leaf


def remove_files(paths, src_folder, target_folder):
    for relPath in paths:
        src_folder = src_folder.replace("**", "")
        encrypted_path = target_folder + relPath + ".gpg"
        if os.path.exists(encrypted_path) and os.path.isfile(encrypted_path):
            os.remove(encrypted_path)


def get_current_unix_ts():
    return str(time.time()).split('.')[0]


def write_bytes_to_file_create_folder(byte_arr, output_path):
    if byte_arr is None:
        logger.critical("attempted to write None for %s", output_path)
        raise Exception("attempted to write None")
    head = calc_path_head(output_path)
    created = create_dirs(head)
    if created:
        logger.info("Created folder: %s for file: %s", head, output_path)
    write_bytes_to_file(byte_arr, output_path)


def write_bytes_to_file(byte_arr, output_path):
    if byte_arr is None:
        logger.critical("attempted to write None for %s", output_path)
        raise Exception("attempted to write None")
    f = open(output_path, 'wb')
    f.write(byte_arr)
    f.close()


def md5(file_path):
    if file_path is None:
        logger.critical("md5(file_path): none is received as agrument")
        return None
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        i = iter(lambda: f.read(4096), b"")
        for chunk in i:
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def md5_from_bytes(my_bytes):
    if my_bytes is None:
        logger.critical("md5_from_bytes: none is received")
        return None
    f = io.BytesIO(my_bytes)
    hash_md5 = hashlib.md5()

    i = iter(lambda: f.read(4096), b"")
    for chunk in i:
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def md5_from_string(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()
