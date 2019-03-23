import os
from src import utils

def git_commit(target_folder):
    previous_cwd =  os.getcwd()
    os.chdir(target_folder)
    utils.execute_command('git add *.gpg')
    utils.execute_command('git commit -m "commited by script"')
    os.chdir(previous_cwd)

def git_clone(target_folder, git_init_url):
    previous_cwd = os.getcwd()
    os.chdir(target_folder)
    utils.execute_command('git clone ' + git_init_url + " .")
    os.chdir(previous_cwd)

def git_pull(repo_folder):
    previous_cwd =  os.getcwd()
    os.chdir(repo_folder)
    utils.execute_command("git pull")
    os.chdir(previous_cwd)