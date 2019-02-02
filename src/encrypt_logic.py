import glob

from src import utils, sync, encrypt, git


def encrypt_run(folder_src, folder_target, state_file):
    files_unencrypted = glob.glob(folder_src, recursive=True)

    current_state = sync.build_md5_files_map_virtual(files_unencrypted, folder_src)
    previous_state = utils.read_json_dict_from_file(state_file)

    if previous_state == current_state:
        print("state is not changed")
        utils.stop_application()

    elements_added = sync.find_added_elements_by_key(current_state, previous_state)
    elements_removed = sync.find_removed_elements_by_key(current_state, previous_state)
    elements_modified = sync.find_modified_files(current_state, previous_state)

    utils.create_target_dir(folder_target)
    utils.create_enc_dir_structure(elements_added.keys(), folder_src, folder_target)
    encrypt.encrypt_files(elements_added.keys(), folder_src, folder_target)
    utils.remove_files(elements_removed.keys(), folder_src, folder_target)
    encrypt.encrypt_files(elements_modified.keys(), folder_src, folder_target)

    utils.dict_to_json(state_file, current_state)
    git.git_commit_and_push(folder_target)

