import os

from src import decrypt_routine, encrypt_routine, utils, git


def handle_group_7(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        relative_path = relative_path.lstrip("/")
        md5_decrypted = md5
        unencrypted_file_path = folder_base_local + "/" + relative_path
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        decrypted_file_contents = decrypt_routine.decrypt_single_file_inmemory(encrypted_file_path)
        md5_encrypted = utils.md5_from_bytes(decrypted_file_contents)
        if os.path.isfile(unencrypted_file_path):
            if md5_encrypted != md5_decrypted:
                encrypt_routine.encrypt_single_file(unencrypted_file_path, encrypted_file_path)
        else:
            print("path is not a file: ", unencrypted_file_path)


def handle_group_8(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        relative_path = relative_path.lstrip("/")
        md5_decrypted = md5
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        decrypted_file_contents = decrypt_routine.decrypt_single_file_inmemory(encrypted_file_path)
        md5_encrypted = utils.md5_from_bytes(decrypted_file_contents)
        if md5_encrypted != md5_decrypted:
            current_ts = utils.get_current_unix_ts()
            utils.write_bytes_to_file(decrypted_file_contents, folder_base_local + "/" + relative_path)


def handle_group_1(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        relative_path = relative_path.lstrip("/")
        md5_decrypted = md5
        unencrypted_file_path = folder_base_local + "/" + relative_path
        if os.path.isdir(unencrypted_file_path):
            continue
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        decrypted_file_contents = decrypt_routine.decrypt_single_file_inmemory(encrypted_file_path)
        md5_encrypted = utils.md5_from_bytes(decrypted_file_contents)
        if md5_encrypted != md5_decrypted:
            current_ts = utils.get_current_unix_ts()
            utils.write_bytes_to_file(decrypted_file_contents, folder_base_local + "/" + current_ts + "_" + relative_path)
            os.rename(encrypted_file_path, folder_base_remote + "/" + current_ts + "_" + relative_path + ".gpg")
            encrypt_routine.encrypt_single_file(unencrypted_file_path, encrypted_file_path)
        else:
            print("files are the same")


def handle_group_3(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        relative_path = relative_path.lstrip("/")
        path_unencrypted = folder_base_local + "/" + relative_path
        path_encrypted_relative = relative_path + ".gpg"
        if os.path.isfile(path_unencrypted):
            deleted_file_contents = git.git_get_recent_file_contents(folder_base_remote, path_encrypted_relative)
            md5_deleted_file = utils.md5_from_bytes(deleted_file_contents)
            md5_existing_file = utils.md5(path_unencrypted)
            if md5_deleted_file == md5_existing_file:
                print("removing " + path_unencrypted)
                os.remove(path_unencrypted)
            else:
                unencrypted_file_path_renamed = folder_base_local + "/" + utils.get_current_unix_ts() + "_" + relative_path
                os.rename(path_unencrypted, unencrypted_file_path_renamed)
        else:
            print("path is not a file: " + path_unencrypted)


def handle_group_6(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        unencrypted_file_path = folder_base_local + "/" + relative_path
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        if os.path.isfile(encrypted_file_path):
            decrypt_routine.decrypt_single_file(encrypted_file_path, unencrypted_file_path)
        else:
            print("path is not a file: " + encrypted_file_path)


def handle_group_5(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        unencrypted_file_path = folder_base_local + "/" + relative_path
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        if os.path.isfile(unencrypted_file_path):
            encrypt_routine.encrypt_single_file(unencrypted_file_path, encrypted_file_path)
        else:
            print("path is not a file: " + unencrypted_file_path)



def handle_group_2_4(relative_paths, folder_base_local, folder_base_remote):
    for relative_path, md5 in relative_paths.items():
        relative_path = relative_path.lstrip("/")
        md5_decrypted = md5
        encrypted_file_path = folder_base_remote + "/" + relative_path + ".gpg"
        if os.path.isfile(encrypted_file_path):
            decrypted_file_contents = decrypt_routine.decrypt_single_file_inmemory(encrypted_file_path)
            md5_encrypted = utils.md5_from_bytes(decrypted_file_contents)
            if md5_encrypted == md5_decrypted:
                os.remove(encrypted_file_path)
            else:
                print("writing conflicted file to local folder")
                current_ts = utils.get_current_unix_ts()
                utils.write_bytes_to_file(decrypted_file_contents, folder_base_local + "/" + current_ts + "_" + relative_path)
                os.rename(encrypted_file_path, folder_base_remote + "/" + current_ts + "_" + relative_path + ".gpg")
        else:
            print(encrypted_file_path + " is not a file")
