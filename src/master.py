import configparser

from src import utils, git, sync, conflict_manager, decrypt_routine

config = configparser.ConfigParser()
config.read('default.conf')

folder_local = config["default"]["dir-unencrypted"]
folder_remote = config["default"]["dir-encrypted"]
git_repo_url = config["default"]["git-repo-url"]
state_file = "state.json"
folder_trash_bin = "__trash_bin"

utils.create_dirs(folder_local)
utils.create_dirs(folder_local + "/" + folder_trash_bin)
repo_just_initialized = utils.create_dirs(folder_remote)
previous_remote_state = sync.calculate_state_without_gpg_ext(folder_remote)

if repo_just_initialized:
    print("Created new repository dir.")
    git.git_clone(folder_remote, git_repo_url)
else:
    git.git_pull(folder_remote)

current_remote_state = sync.calculate_state_without_gpg_ext(folder_remote)

current_local_state = sync.calculate_state_without_trash_bin(folder_local, folder_trash_bin)
previous_local_state = utils.read_json_dict_from_file(state_file)

# calculate operations

decrypt_to_left_no_conflicts = conflict_manager.decrypt_to_left_no_conflicts(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
on_left_to_trash_bin = conflict_manager.on_left_to_trash_bin(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
on_right_remove = conflict_manager.on_right_remove(previous_remote_state, current_remote_state, previous_local_state, current_local_state)


# execute operations

sync.check_conflict_and_remove_on_right(on_right_remove, folder_local, folder_remote)
decrypt_routine.decrypt_gpged_files(decrypt_to_left_no_conflicts, folder_local, folder_remote)
sync.move_to_trash_bin(on_left_to_trash_bin, folder_local)
