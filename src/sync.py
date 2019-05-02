import hashlib
import os
import glob
import time
from src import decrypt_routine

def remove_gpg_ext(list_files):
    result = {}
    for key, value in list_files.items():
        new_key = replace_last(key, ".gpg", "")
        result[new_key] = value
    return result


def build_md5_files_map_virtual_remove_gpg_ext(list_files, folder_src):
    list_files = build_md5_files_map_virtual(list_files, folder_src)
    return remove_gpg_ext(list_files)


def calculate_state_without_trash_bin(folder_path, folder_trash_bin_path):
    state = calculate_state(folder_path)
    result = {}
    for key, value, in state.items():
        if folder_trash_bin_path not in key:
            result[key] = value
    return result


def calculate_state(folder_path):
    list_files = glob.glob(folder_path + "/**", recursive=True)
    return build_md5_files_map_virtual(list_files, folder_path)


def calculate_state_without_gpg_ext(folder_path):
    list_files = glob.glob(folder_path + "/**", recursive=True)
    return build_md5_files_map_virtual_remove_gpg_ext(list_files, folder_path)


def build_md5_files_map_virtual(list_files, folder_src):
    folder_src = folder_src.replace("*", "")
    result = {}
    for file in list_files:
        file_rel = os.path.relpath(file, folder_src)
        file_rel = "/" + file_rel.replace("\\", "/")  # windows-specific
        if file_rel == "/.":
            continue
        if os.path.isfile(file):
            filemd5 = md5(file)
            result[file_rel] = filemd5
        if os.path.isdir(file):
            file_rel = file_rel + "/"
            md5_from_dir_path = md5_from_string(file_rel)
            result[file_rel] = md5_from_dir_path
    return result


def find_diff_by_key(dict1, dict2):
    return {k: dict1[k] for k in set(dict1) - set(dict2)}


def find_modified_files(dict1, dict2):
    same_names = find_intersection_by_keys(dict1, dict2)  # files that have the same names but may was modified
    same1 = find_intersection_by_keys(dict1, same_names)
    same2 = find_intersection_by_keys(dict2, same_names)
    diff = set(same1.values()) - set(same2.values())
    swapped = {v: k for k, v in dict1.items()}
    result = {swapped[i]: i for i in diff}
    return result


def find_not_modified_files(dict1, dict2):
    same_names = find_intersection_by_keys(dict1, dict2)
    same1 = find_intersection_by_keys(dict1, same_names)
    same2 = find_intersection_by_keys(dict2, same_names)
    diff = set(same1.values()).intersection(set(same2.values()))
    swapped = {v: k for k, v in dict1.items()}
    result = {swapped[i]: i for i in diff}
    return result


def find_intersection_by_keys(dict1, dict2):
    return {k: dict1[k] for k in set(dict1).intersection(set(dict2))}


def find_added_elements_by_key(dict1, dict2):
    return find_diff_by_key(dict1, dict2)


def find_removed_elements_by_key(dict1, dict2):
    return find_diff_by_key(dict2, dict1)


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        i = iter(lambda: f.read(4096), b"")
        for chunk in i:
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def md5_bytes(bytes):
    f = io.BytesIO()
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        i = iter(lambda: f.read(4096), b"")
        for chunk in i:
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def md5_from_string(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail


def move_to_trash_bin(relative_paths, base_path):
    for relative_path in relative_paths:
        os.rename(base_path + "/" + relative_path, base_path + "__trash_bin" + relative_path + "_" + str(time.time()))

def check_conflict_and_remove_on_right(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        md5_decrypted = md5
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        decrypted_file_contents = decrypt_routine.decrypt_single_file_inmemory_to_str(encrypted_file_path)
        md5_encrypted = md5_from_string(decrypted_file_contents)
        if md5_encrypted == md5_decrypted:
            print('123')

