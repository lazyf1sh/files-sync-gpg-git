import hashlib
import os


def build_md5_files_map_virtual(list_files):
    result = {}
    for file in list_files:
        if os.path.isfile(file):
            filemd5 = md5(file)
            result[file] = filemd5
        if os.path.isdir(file):
            md5_from_dir_path = md5_from_string(file)
            result[file] = md5_from_dir_path
    return result


def find_diff_by_key(dict1, dict2):
    return {k: dict1[k] for k in set(dict1) - set(dict2)}


def find_modified_files(dict1, dict2):
    same_names = find_intersection_by_keys(dict1, dict2)  # files that have the same names but may be modified
    same1 = find_intersection_by_keys(dict1, same_names)
    same2 = find_intersection_by_keys(dict2, same_names)
    diff = set(same1.values()) - set(same2.values())
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
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def md5_from_string(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()
