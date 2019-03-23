import sys
from src import decrypt_logic, encrypt_logic, utils, git, sync, conflict_manager, RenameStrategy
import configparser
import glob

config = configparser.ConfigParser()
config.read('default.conf')

folder_local = config["default"]["dir-unencrypted"]
folder_remote = config["default"]["dir-encrypted"]
git_repo_url = config["default"]["git-repo-url"]
state_file = "state.json"

#

utils.create_dirs(folder_local)
created = utils.create_dirs(folder_remote)
if created:
    print("Created NEW repository dir")
    print("Cloning existing repo")
    git.git_clone(folder_remote, git_repo_url)

list_files_local = glob.glob(folder_local + "/**", recursive=True)

current_local_state = sync.build_md5_files_map_virtual(list_files_local, folder_local)
previous_local_state = utils.read_json_dict_from_file(state_file)

local_elements_added = sync.find_added_elements_by_key(current_local_state, previous_local_state)
local_elements_removed = sync.find_removed_elements_by_key(current_local_state, previous_local_state)
local_elements_modified = sync.find_modified_files(current_local_state, previous_local_state)

#

list_files_remote = glob.glob(folder_remote + "/**", recursive=True)
previous_remote_state = sync.build_md5_files_map_virtual(list_files_remote, folder_remote)
previous_remote_state = sync.removeGpgExtension(previous_remote_state)

if not created:
    git.git_pull(folder_remote)

list_files_remote = glob.glob(folder_remote + "/**", recursive=True)
current_remote_state = sync.build_md5_files_map_virtual(list_files_remote, folder_remote)
current_remote_state = sync.removeGpgExtension(current_remote_state)

remote_elements_added = sync.find_added_elements_by_key(current_remote_state, previous_remote_state)
remote_elements_removed = sync.find_removed_elements_by_key(current_remote_state, previous_remote_state)
remote_elements_modified = sync.find_modified_files(current_remote_state, previous_remote_state)