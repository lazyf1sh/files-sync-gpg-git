import logging
import subprocess
import sys
import tempfile

from src.script import proc_runner

logger = logging.getLogger(__name__)


def git_current_commit(repo_folder):
    logger.info("git_current_commit - start")
    result = proc_runner.execute_command_string("git rev-parse --verify HEAD", repo_folder)
    result = result.replace("\n", "")
    logger.info("git_current_commit - result: %s", result)
    return result


def dir_is_repository(catalog):
    logger.info("git_ping - start")
    try:
        result = proc_runner.execute_command_args_bytes(['git', 'status'], catalog)
        if "on branch" in str(result).lower():
            return True
    except subprocess.CalledProcessError as exc:
        if exc.returncode == 128:
            logger.info("%s is not git repo", catalog)
    return False


def git_init(catalog):
    logger.info("git_init - start")
    result = proc_runner.execute_command_string('git init', catalog)
    logger.info("git_init - result: %s", result)
    return result


def git_ping(repo_folder, remote_repo_url):
    logger.info("git_ping - start")
    result = proc_runner.execute_command_string("git ls-remote -h " + remote_repo_url, repo_folder)
    logger.info("git_ping - result: %s", result)
    return "not found" not in result


def git_status(repo_folder):
    result = proc_runner.execute_command_string('git status', repo_folder)
    logger.info("git_status - result: %s", result)
    return result


def git_add_gpg_files(repo_folder):
    proc_runner.execute_command_string('git add *.gpg', repo_folder)


def git_add_all(repo_folder):
    proc_runner.execute_command_string('git add .', repo_folder)


def git_commit(repo_folder, msg):
    logger.info("git_commit_gpg_files - start")
    result = proc_runner.execute_command_string('git commit -m "' + msg + '"', repo_folder)
    logger.info("git_commit_gpg_files - result: %s", result)
    logger.info("git_commit_gpg_files - end")


def git_clone(repo_folder, git_init_url):
    logger.info("git_clone - start")
    logger.info("Cloning existing repo %s to %s", git_init_url, repo_folder)
    proc_runner.execute_command_string('git clone ' + git_init_url + " .", repo_folder)
    logger.info("git_clone - end")


def git_pull(repo_folder):
    logger.info("git_pull - start")
    result = proc_runner.execute_command_args_bytes(['git', 'pull'], repo_folder)
    logger.info("git_pull - output: %s", result)
    logger.info("git_pull - end")


def git_push(repo_folder):
    logger.info("git_push - start")
    string = proc_runner.execute_command_string("git push", repo_folder)
    logger.info("git_push - output: %s\n", string)
    logger.info("git_push - end")


def git_file_pre_deleted_state_commit_hash(repo_folder, path):
    history = proc_runner.execute_command_args(['git', 'log', '-p', '--', path], repo_folder)
    lines = history.split("\n")
    if len(lines) < 2:
        lines = history.split("\\n")
    logger.info("Lines size: %s", len(lines))
    commit_hash = None
    for line in lines:
        if line.startswith("commit"):
            commit_hash = line.split(" ")[1]
        if line.startswith("index"):
            if "0000000" not in line.split("..")[1]:
                logger.info("Calculated commit before deletion: %s", commit_hash)
                return commit_hash
    logger.error("Unable to read file history: %s", history)
    return None


def git_get_recent_file_data_piped(repo_folder, path) -> bytes:
    """
    Returns previous not deleted file contents
    :param repo_folder:
    :param path:
    """
    commit_hash = git_file_pre_deleted_state_commit_hash(repo_folder, path)
    logger.info("git_get_recent_file_contents(). Running for platform: %s", sys.platform)
    git_command = ['git', 'show', "{}:{}".format(commit_hash, path)]
    gpg_command = ['gpg', '--decrypt']
    file_contents = proc_runner.run_piped(repo_folder, git_command, gpg_command)
    logger.info("decrypted contents: %s", file_contents)
    return file_contents


def git_is_available():
    try:
        output = proc_runner.execute_command_args(['git', '--version'], tempfile.gettempdir())
        logger.debug("git check response: %s", output)
        gpg_lines = output.split("\n")
        if len(gpg_lines) > 1 and "git version" in gpg_lines[0]:
            logger.info(gpg_lines[0])
            return True
        else:
            logger.critical("git is not available")
    except subprocess.CalledProcessError as e:
        logger.critical("error getting git version", e)
    return False
