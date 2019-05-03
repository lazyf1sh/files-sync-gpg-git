import hashlib
import os
import glob
import time
import io
from src import decrypt_routine, encrypt, utils

def remove_gpg_ext(list_files):
    result = {}
    for key, value in list_files.items():
        new_key = replace_last(key, ".gpg", "")
        result[new_key] = value
    return result


def build_md5_files_map_virtual_remove_gpg_ext(list_files, folder_src):
    list_files = build_md5_files_map_virtual(list_files, folder_src)
    return remove_gpg_ext(list_files)


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

def md5_from_bytes(bytes):
    f = io.BytesIO(bytes)
    hash_md5 = hashlib.md5()

    i = iter(lambda: f.read(4096), b"")
    for chunk in i:
        hash_md5.update(chunk)
    return hash_md5.hexdigest()

def md5_from_string(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail


def write_bytes_to_file(bytes, output_path):
    f = open(output_path, 'wb')
    f.write(bytes)
    f.close()


def handle_group_1(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        relative_path = relative_path.lstrip("/")
        md5_decrypted = md5
        uncrypted_file_path = folder_base_local + "/" + relative_path
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        decrypted_file_contents = decrypt_routine.decrypt_single_file_inmemory(encrypted_file_path)
        md5_encrypted = md5_from_bytes(decrypted_file_contents)
        if md5_encrypted != md5_decrypted:
            current_ts = utils.getCurrentTs()
            write_bytes_to_file(decrypted_file_contents, folder_base_local + "/" + current_ts + "_" + relative_path)
            os.rename(folder_base_remote + "/" + relative_path + ".gpg", folder_base_remote + "/" + current_ts + "_" + relative_path + ".gpg")
            encrypt.encrypt_single_file(uncrypted_file_path, encrypted_file_path)
        else:
            print("files are the same")

def handle_group_3(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        relative_path = relative_path.lstrip("/")
        uncrypted_file_path = folder_base_local + "/" + relative_path
        uncrypted_file_path_renamed = folder_base_local + "/" + "DELETED_" + relative_path
        os.rename(uncrypted_file_path, uncrypted_file_path_renamed)


def handle_group_6(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        uncrypted_file_path = folder_base_local + "/" + relative_path
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        decrypt_routine.decrypt_single_file(encrypted_file_path, uncrypted_file_path)

def handle_group_5(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        uncrypted_file_path = folder_base_local + "/" + relative_path
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        encrypt.encrypt_single_file(uncrypted_file_path, encrypted_file_path)

def handle_group_2_4(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        relative_path = relative_path.lstrip("/")
        md5_decrypted = md5
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        decrypted_file_contents = decrypt_routine.decrypt_single_file_inmemory(encrypted_file_path)
        md5_encrypted = md5_from_bytes(decrypted_file_contents)
        if md5_encrypted == md5_decrypted:
            os.remove(encrypted_file_path)
        else:
            print("writing conflicted file to local folder")
            current_ts = utils.getCurrentTs()
            write_bytes_to_file(decrypted_file_contents, folder_base_local + "/" + current_ts + "_" + relative_path)
            os.rename(folder_base_remote + "/" + relative_path + ".gpg", folder_base_remote + "/" + current_ts + "_" + relative_path + ".gpg")