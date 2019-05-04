from src import utils


def git_status(target_folder):
    result = utils.execute_command('git status', target_folder)
    return result


def git_commit_gpg_files(target_folder):
    utils.execute_command('git add .', target_folder)
    utils.execute_command('git commit -m "commited by script"', target_folder)


def git_clone(target_folder, git_init_url):
    print("Cloning existing repo.")
    utils.execute_command('git clone ' + git_init_url + " .", target_folder)


def git_pull(repo_folder):
    utils.execute_command("git pull", repo_folder)


def git_push(repo_folder):
    print("push the data to the repository.")
    utils.execute_command("git push", repo_folder)
    print("pushed the data from repository.")
