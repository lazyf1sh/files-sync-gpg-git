import os
from src import utils

def git_commit_and_push(target_folder):
    previous_cwd =  os.getcwd()
    os.chdir(target_folder)
    utils.execute_command('git add *.gpg')
    utils.execute_command('git commit -m upd')
    os.chdir(previous_cwd)