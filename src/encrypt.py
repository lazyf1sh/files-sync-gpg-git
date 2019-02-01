import os
import subprocess
import shlex

recipient = "94B31905EEA476BA62B105D0BBDC9AD25A5BEF95!"


def execute_command(command):
    args = shlex.split(command)
    try:
        proc = subprocess.check_output(args)
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)
        return
    else:
        print("Output: \n{}\n".format(proc))


def git_commit_and_push(target_folder):
    previous_cwd = os.getcwd()
    os.chdir(target_folder)
    execute_command('git add *.gpg')
    execute_command('git commit -m upd')
    os.chdir(previous_cwd)


def encrypt_files(list_files, src_folder, target_folder):
    for relPath in list_files:
        absPath = src_folder.replace("*", "") + relPath
        if os.path.isfile(absPath) and not absPath.lower().endswith('.gpg'):
            path_encrypted = target_folder + relPath
            print(subprocess.check_output(['gpg', '--yes', '--verbose', '--output', path_encrypted + '.gpg', '--encrypt', '--recipient', recipient, absPath]))
