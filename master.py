import configparser
import logging.config
import os
import sys

from src.script import sync, utils, git, operations_calculator, executor_folders, executor_files

lock_file_path = "state/lock"
previous_run_success = True

if os.path.exists(lock_file_path) and  os.path.isfile(lock_file_path):
    previous_run_success = False

f = open(lock_file_path, "w+")

main_conf = sys.argv[1]
logging_conf = sys.argv[2]

logging.config.fileConfig(logging_conf)
logger = logging.getLogger(__name__)


config = configparser.ConfigParser()
config.read(main_conf)

folder_local = config["default"]["dir-unencrypted"]
folder_remote = config["default"]["dir-encrypted"]
git_repo_url = config["default"]["git-repo-url"]
state_file = "state/state.json"

logger.info("state file: %s", state_file)
logger.info("git_repo_url: %s", git_repo_url)
logger.info("folder_remote: %s", folder_remote)
logger.info("folder_local: %s", folder_local)
logger.info("--------------- script launched ---------------")

utils.create_dirs(folder_local)
repo_just_initialized = utils.create_dirs(folder_remote)
previous_remote_state = sync.calculate_state_without_gpg_ext(folder_remote)

if repo_just_initialized:
    logger.info("Created new repository dir. Cloning repo")
    git.git_clone(folder_remote, git_repo_url)
else:
    git.git_pull(folder_remote)

current_remote_state = sync.calculate_state_without_gpg_ext(folder_remote)

current_local_state = sync.calculate_state(folder_local)
previous_local_state = utils.read_json_dict_from_file(state_file)

if current_remote_state == previous_remote_state and current_local_state == previous_local_state:
    logger.info("states are the same")
    utils.stop_application(f, lock_file_path)

# calculate operations
logger.info("calculating operations - start")
group_1 = operations_calculator.group_1(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
group_2_4 = operations_calculator.group_2_4(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
group_3 = operations_calculator.group_3(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
group_5 = operations_calculator.group_5(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
group_6 = operations_calculator.group_6(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
group_7 = operations_calculator.group_7(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
group_8 = operations_calculator.group_8(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
logger.info("calculating operations - end")

# execute operations for folders
executor_folders.create_remote_dirs(group_5, folder_local, folder_remote)
executor_folders.create_remote_dirs(group_1, folder_local, folder_remote)
executor_folders.create_local_dirs(group_6, folder_local, folder_remote)

# execute operations for files
executor_files.handle_group_3(group_3, folder_local, folder_remote)  # remote deletion
executor_files.handle_group_2_4(group_2_4, folder_local, folder_remote)  # local deletion
executor_files.handle_group_6(group_6, folder_local, folder_remote)  # not existed local
executor_files.handle_group_5(group_5, folder_local, folder_remote)  # not existed remote
if not previous_run_success:
    executor_files.handle_group_1(group_1, folder_local, folder_remote)  # checking conflicts through existing files. place for optimizations
executor_files.handle_group_7(group_7, folder_local, folder_remote)  # modified local, not modified remote
executor_files.handle_group_8(group_8, folder_local, folder_remote)  # modified remote, not modified local

# execute operations for folders
executor_folders.remove_remote_dirs(group_2_4, folder_remote)
executor_folders.remove_remote_dirs(group_3, folder_remote)

status_string = git.git_status(folder_remote)
if "nothing to commit" not in status_string:
    git.git_add_gpg_files(folder_remote)
    git.git_status(folder_remote)
    git.git_commit(folder_remote)
    git.git_push(folder_remote)
else:
    logger.info(status_string)

sync.save_current_state(state_file, current_local_state)
utils.stop_application(f, lock_file_path)

