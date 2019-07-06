import os

from src import utils


def handle_group_5_folders(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        unencrypted_folder_path = folder_base_local + "/" + relative_path
        if os.path.isdir(unencrypted_folder_path):
            repo_folder_path = folder_base_remote + "/" + relative_path
            utils.create_dirs(repo_folder_path)
        else:
            print("path is not a dir: " + unencrypted_folder_path)


def handle_group_6_folders(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        repo_folder_path = folder_base_remote + "/" + relative_path
        if os.path.isdir(repo_folder_path):
            unencrypted_folder_path = folder_base_local + "/" + relative_path
            utils.create_dirs(unencrypted_folder_path)
