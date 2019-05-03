import os
from src import utils

def git_status(target_folder):
    previous_cwd = os.getcwd()
    os.chdir(target_folder)
    return utils.execute_command('git status')
    os.chdir(previous_cwd)


def git_commit_gpg_files(target_folder):
    previous_cwd = os.getcwd()
    os.chdir(target_folder)
    utils.execute_command('git add *.gpg')
    utils.execute_command('git commit -m "commited by script"')
    os.chdir(previous_cwd)


def git_clone(target_folder, git_init_url):
    previous_cwd = os.getcwd()
    os.chdir(target_folder)
    print("Cloning existing repo.")
    utils.execute_command('git clone ' + git_init_url + " .")
    print("Cloned existing repo.")
    os.chdir(previous_cwd)


def git_pull(repo_folder):
    previous_cwd = os.getcwd()
    os.chdir(repo_folder)
    print("pulling the data from repository.")
    utils.execute_command("git pull")
    print("pulled the data repository.")
    os.chdir(previous_cwd)

def git_push(repo_folder):
    previous_cwd = os.getcwd()
    os.chdir(repo_folder)
    print("push the data to the repository.")
    utils.execute_command("git push")
    print("pushed the data from repository.")
    os.chdir(previous_cwd)