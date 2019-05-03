import configparser

from src import utils, git, sync, conflict_manager, decrypt_routine

config = configparser.ConfigParser()
config.read('default.conf')

folder_local = config["default"]["dir-unencrypted"]
folder_remote = config["default"]["dir-encrypted"]
git_repo_url = config["default"]["git-repo-url"]
state_file = "state.json"

utils.create_dirs(folder_local)
repo_just_initialized = utils.create_dirs(folder_remote)
previous_remote_state = sync.calculate_state_without_gpg_ext(folder_remote)

if repo_just_initialized:
    print("Created new repository dir.")
    git.git_clone(folder_remote, git_repo_url)
else:
    git.git_pull(folder_remote)

current_remote_state = sync.calculate_state_without_gpg_ext(folder_remote)

current_local_state = sync.calculate_state(folder_local)
previous_local_state = utils.read_json_dict_from_file(state_file)

if current_remote_state == previous_remote_state and current_local_state == previous_local_state:
    print("state is not changed")
    # utils.stop_application()

# calculate operations
group_1 = conflict_manager.group_1(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
group_2_4 = conflict_manager.group_2_4(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
group_3 = conflict_manager.group_3(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
group_5 = conflict_manager.group_5(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
group_6 = conflict_manager.group_6(previous_remote_state, current_remote_state, previous_local_state, current_local_state)

# execute operations
sync.handle_group_3(group_3, folder_local, folder_remote) #
sync.handle_group_6(group_6, folder_local, folder_remote) #
sync.handle_group_5(group_5, folder_local, folder_remote) #
sync.handle_group_2_4(group_2_4, folder_local, folder_remote) # local deletion
sync.handle_group_1(group_1, folder_local, folder_remote) # current state

utils.dict_to_json(state_file, current_local_state)
git.git_commit(folder_remote)