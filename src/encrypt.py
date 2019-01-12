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
    for file in list_files:
        if os.path.isfile(file) and not file.lower().endswith('.gpg'):
            src_folder = src_folder.replace("**", "")
            path_encrypted = target_folder + os.path.relpath(file, src_folder)
            print(subprocess.check_output(['gpg', '--yes', '--verbose', '--output', path_encrypted + '.gpg', '--encrypt', '--recipient', recipient, file]))
