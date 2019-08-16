import logging
import os

from src.script import utils
from src.script import gpg
from src.script import git

logger = logging.getLogger(__name__)


def handle_group_7(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        relative_path = relative_path.lstrip("/")
        md5_decrypted = md5
        unencrypted_file_path = folder_base_local + "/" + relative_path
        if os.path.isfile(unencrypted_file_path):
            encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
            decrypted_file_bytes = gpg.decrypt_single_file_inmemory(encrypted_file_path, folder_base_remote)
            md5_encrypted = utils.md5_from_bytes(decrypted_file_bytes)
            if md5_encrypted != md5_decrypted:
                logger.info("group 7: encrypting %s", relative_path)
                gpg.encrypt_single_file(unencrypted_file_path, encrypted_file_path, folder_base_remote)
            else:
                logger.info("group 7: files are the same - no re-encrypting required: %s", relative_path)
        else:
            logger.debug("group 7: path is not a file: ", relative_path)


def handle_group_8(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        relative_path = relative_path.lstrip("/")
        md5_decrypted = md5
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        if os.path.isfile(encrypted_file_path):
            decrypted_file_contents = gpg.decrypt_single_file_inmemory(encrypted_file_path, folder_base_remote)
            md5_encrypted = utils.md5_from_bytes(decrypted_file_contents)
            if md5_encrypted != md5_decrypted:
                logger.info("group 8: unpacking file: %s", relative_path)
                utils.write_bytes_to_file_create_folder(decrypted_file_contents, folder_base_local + "/" + relative_path)
            else:
                logger.debug("group 8: files are the same - no action required: %s", relative_path)
        else:
            logger.debug("group 8: path is not a file: ", relative_path)


def handle_group_1(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        relative_path = relative_path.lstrip("/")
        md5_decrypted = md5
        unencrypted_file_path = folder_base_local + "/" + relative_path
        if os.path.isdir(unencrypted_file_path):
            logger.debug("group 1: path is not a file: ", relative_path)
            continue
        logger.debug("group 1: checking %s", relative_path)
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        decrypted_file_contents = gpg.decrypt_single_file_inmemory(encrypted_file_path, folder_base_remote)
        md5_encrypted = utils.md5_from_bytes(decrypted_file_contents)
        if md5_encrypted != md5_decrypted:
            logger.info("group 1: handling conflict: %s", relative_path)
            current_ts = utils.get_current_unix_ts()
            utils.write_bytes_to_file_create_folder(decrypted_file_contents, utils.append_ts_to_path(unencrypted_file_path, current_ts))
            os.rename(encrypted_file_path, utils.append_ts_to_path(encrypted_file_path, current_ts))
            gpg.encrypt_single_file(unencrypted_file_path, encrypted_file_path, folder_base_remote)
        else:
            logger.debug("group 1: files are the same: %s", relative_path)


def handle_group_3(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        relative_path = relative_path.lstrip("/")
        path_unencrypted = folder_base_local + "/" + relative_path
        path_encrypted_relative = relative_path + ".gpg"
        if os.path.isfile(path_unencrypted):
            logger.debug("group 3: checking %s", relative_path)
            deleted_file_contents = git.git_get_recent_file_contents(folder_base_remote, path_encrypted_relative)
            md5_deleted_file = utils.md5_from_bytes(deleted_file_contents)
            md5_existing_file = utils.md5(path_unencrypted)
            if md5_deleted_file == md5_existing_file:
                logger.info("group 3: removing %s", path_unencrypted)
                os.remove(path_unencrypted)
            else:
                unencrypted_file_path_renamed = utils.append_ts_to_path(path_unencrypted, utils.get_current_unix_ts())
                os.rename(path_unencrypted, unencrypted_file_path_renamed)
        else:
            logger.debug("group 3: path is not a file: " + path_unencrypted)


def handle_group_6(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        unencrypted_file_path = folder_base_local + "/" + relative_path
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        if os.path.isfile(encrypted_file_path):
            logger.debug("group 6: %s", relative_path)
            gpg.decrypt_single_file(encrypted_file_path, unencrypted_file_path)
        else:
            logger.debug("path is not a file: " + encrypted_file_path)


def handle_group_5(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        unencrypted_file_path = folder_base_local + "/" + relative_path
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        if os.path.isfile(unencrypted_file_path):
            logger.debug("group 5: %s", relative_path)
            gpg.encrypt_single_file(unencrypted_file_path, encrypted_file_path, folder_base_remote)
        else:
            logger.debug("path is not a file: " + unencrypted_file_path)


def handle_group_2_4(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        relative_path = relative_path.lstrip("/")
        md5_decrypted = md5
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        if os.path.isfile(encrypted_file_path):
            logger.debug("group 2_4: %s", relative_path)
            decrypted_file_contents = gpg.decrypt_single_file_inmemory(encrypted_file_path, folder_base_remote)
            md5_encrypted = utils.md5_from_bytes(decrypted_file_contents)
            if md5_encrypted == md5_decrypted:
                os.remove(encrypted_file_path)
            else:
                logger.info("writing conflicted file to local folder: %s", relative_path)
                current_ts = utils.get_current_unix_ts()
                decrypt_path = utils.append_ts_to_path(folder_base_local + "/" + relative_path, current_ts)
                remote_rename_path = utils.append_ts_to_path(folder_base_remote + "/" + relative_path + ".gpg", current_ts)

                logger.info("decrypt path: %s", decrypt_path)
                logger.info("remote rename path: %s", remote_rename_path)
                utils.write_bytes_to_file_create_folder(decrypted_file_contents, decrypt_path)
                os.rename(encrypted_file_path, remote_rename_path)
        else:
            logger.debug(encrypted_file_path + " is not a file")
