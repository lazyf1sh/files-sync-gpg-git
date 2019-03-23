import configparser

from src import utils, git, sync

config = configparser.ConfigParser()
config.read('default.conf')

folder_local = config["default"]["dir-unencrypted"]
folder_remote = config["default"]["dir-encrypted"]
git_repo_url = config["default"]["git-repo-url"]
state_file = "state.json"

#

previous_remote_state = {}

utils.create_dirs(folder_local)
created = utils.create_dirs(folder_remote)
if created:
    print("Created NEW repository dir. Cloning existing repo.")
    previous_remote_state = sync.calculate_state_without_gpg_ext(folder_remote)
    git.git_clone(folder_remote, git_repo_url)

current_local_state = sync.calculate_state(folder_local)
previous_local_state = utils.read_json_dict_from_file(state_file)

local_elements_added = sync.find_added_elements_by_key(current_local_state, previous_local_state)
local_elements_removed = sync.find_removed_elements_by_key(current_local_state, previous_local_state)
local_elements_modified = sync.find_modified_files(current_local_state, previous_local_state)

#
if len(previous_remote_state) == 0:
    previous_remote_state = sync.calculate_state_without_gpg_ext(folder_remote)

if not created:
    git.git_pull(folder_remote)

current_remote_state = sync.calculate_state_without_gpg_ext(folder_remote)

remote_elements_added = sync.find_added_elements_by_key(current_remote_state, previous_remote_state)
remote_elements_removed = sync.find_removed_elements_by_key(current_remote_state, previous_remote_state)
remote_elements_modified = sync.find_modified_files(current_remote_state, previous_remote_state)
