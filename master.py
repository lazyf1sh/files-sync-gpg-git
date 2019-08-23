import configparser
import logging.config
import os
import sys

from src.script import sync, utils, git, operations_calculator, executor_folders, executor_files, gpg

if len(sys.argv) < 2:
    print("missing arguments")
    sys.exit(1)

main_conf = sys.argv[1]
logging_conf = sys.argv[2]

config = configparser.ConfigParser()
config.read(main_conf)

dir_unencrypted = config["default"]["dir-unencrypted"]
dir_encrypted = config["default"]["dir-encrypted"]
git_repo_url = config["default"]["git-repo-url"]
state_file = "state/state.json"

utils.create_dirs("state")
utils.create_dirs("logs")

logging.config.fileConfig(logging_conf)
logger = logging.getLogger(__name__)

logger.info("--------------- script launched ---------------")

gpg_is_installed = gpg.gpg_is_available()
if not gpg_is_installed:
    logger.critical("gpg is not installed")
    utils.stop_script_no_args()

# check gpg has defined key

git_is_installed = git.git_is_available()
if not git_is_installed:
    logger.critical("git is not installed")
    utils.stop_script_no_args()

# git check user / email are customzed

lock_file_path = "state/lock"
previous_run_success = True
if os.path.exists(lock_file_path) and os.path.isfile(lock_file_path):
    logger.critical("Previous run was not successful")
    previous_run_success = False

f = open(lock_file_path, "w+")

if dir_unencrypted == dir_encrypted:
    logger.critical("Customizing error: repo folder and working folders cannot point to the same location")
    utils.stop_script(f, lock_file_path)

logger.info("state file: %s", state_file)
logger.info("git_repo_url: %s", git_repo_url)
logger.info("folder_remote: %s", dir_encrypted)
logger.info("folder_local: %s", dir_unencrypted)

utils.create_dirs(dir_unencrypted)
repo_just_initialized = utils.create_dirs(dir_encrypted)

ping_successful = git.git_ping(dir_encrypted, git_repo_url)
if not ping_successful:
    utils.stop_script(f, lock_file_path)

previous_remote_state = sync.calculate_state_without_gpg_ext(dir_encrypted)

if repo_just_initialized:
    logger.info("Created new repository dir. Cloning repo")
    sync.save_state(state_file, {})
    # check folder is empty before cloning
    # check git is not initialized before cloning
    git.git_clone(dir_encrypted, git_repo_url)
else:
    status_str = git.git_status(dir_encrypted)
    if "on branch" in status_str.lower():
        git.git_pull(dir_encrypted)

current_remote_state = sync.calculate_state_without_gpg_ext(dir_encrypted)

current_local_state = sync.calculate_state(dir_unencrypted)
previous_local_state = utils.read_json_dict_from_file(state_file)

if current_remote_state == previous_remote_state and current_local_state == previous_local_state:
    logger.info("states are the same")
    utils.stop_script(f, lock_file_path)

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
executor_folders.create_remote_dirs(group_5, dir_unencrypted, dir_encrypted)
executor_folders.create_remote_dirs(group_1, dir_unencrypted, dir_encrypted)
executor_folders.create_local_dirs(group_6, dir_unencrypted, dir_encrypted)

# execute operations for files
executor_files.handle_group_3(group_3, dir_unencrypted, dir_encrypted)  # remote deletion
executor_files.handle_group_2_4(group_2_4, dir_unencrypted, dir_encrypted)  # local deletion
executor_files.handle_group_6(group_6, dir_unencrypted, dir_encrypted)  # not existed local
executor_files.handle_group_5(group_5, dir_unencrypted, dir_encrypted)  # not existed remote
if not previous_run_success:
    executor_files.handle_group_1(group_1, dir_unencrypted, dir_encrypted)  # checking conflicts through existing files. place for optimizations
executor_files.handle_group_7(group_7, dir_unencrypted, dir_encrypted)  # modified local, not modified remote
executor_files.handle_group_8(group_8, dir_unencrypted, dir_encrypted)  # modified remote, not modified local

# execute operations for folders
executor_folders.remove_remote_dirs(group_2_4, dir_encrypted)
executor_folders.remove_local_dirs(group_3, dir_unencrypted)

status_string = git.git_status(dir_encrypted)
if "nothing to commit" not in status_string:
    git.git_add_gpg_files(dir_encrypted)
    git.git_status(dir_encrypted)
    git.git_commit(dir_encrypted)
    git.git_push(dir_encrypted)
    commit = git.git_current_commit(dir_encrypted)
else:
    logger.info(status_string)

sync.save_state(state_file, current_local_state)
utils.stop_script(f, lock_file_path)
