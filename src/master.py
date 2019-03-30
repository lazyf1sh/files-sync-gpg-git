import configparser

from src import utils, git, sync, conflict_manager

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

conflict_manager.do_resolve(previous_remote_state, current_remote_state, previous_local_state, current_local_state)