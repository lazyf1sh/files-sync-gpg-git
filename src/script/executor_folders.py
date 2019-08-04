import logging
import os

from src.script import utils


logger = logging.getLogger(__name__)


def create_remote_dirs(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        unencrypted_folder_path = folder_base_local + "/" + relative_path
        if os.path.isdir(unencrypted_folder_path):
            repo_folder_path = folder_base_remote + "/" + relative_path
            utils.create_dirs(repo_folder_path)
        else:
            logger.debug("path is not a dir: %s", unencrypted_folder_path)


def create_local_dirs(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        repo_folder_path = folder_base_remote + "/" + relative_path
        if os.path.isdir(repo_folder_path):
            unencrypted_folder_path = folder_base_local + "/" + relative_path
            utils.create_dirs(unencrypted_folder_path)


def remove_remote_dirs(relative_paths, folder_base_remote):
    sorted_list = sorted(relative_paths, reverse=True)
    for relative_path in sorted_list:
        repo_folder_path = folder_base_remote + "/" + relative_path
        if os.path.isdir(repo_folder_path):
            utils.remove_dirs(repo_folder_path)
        else:
            logger.debug("path is not a dir: %s", repo_folder_path)


def remove_local_dirs(relative_paths, dir_base_local_path):
    sorted_list = sorted(relative_paths, reverse=True)
    for relative_path in sorted_list:
        local_dir_path = dir_base_local_path + "/" + relative_path
        if os.path.isdir(local_dir_path):
            utils.remove_dirs(local_dir_path)
        else:
            logger.debug("path is not a dir: %s", local_dir_path)
