import csv
import glob
import hashlib
import json
import os
import subprocess
import shlex
import pickle
import pprint

recipient = "94B31905EEA476BA62B105D0BBDC9AD25A5BEF95!"

def executeCommand(command):
    args = shlex.split(command)
    try:
        proc = subprocess.check_output(args)
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)
        return
    else:
        print("Output: \n{}\n".format(proc))


def gitcommitAndPush(targetFolder):
    previous_cwd = os.getcwd()
    os.chdir(targetFolder)
    executeCommand('git add *.gpg')
    executeCommand('git commit -m upd')
    os.chdir(previous_cwd)


def encrypt_files(files_enencrypted, srcFolder, targetFolder):
    for file in files_enencrypted:
        if os.path.isfile(file) and not file.lower().endswith('.gpg'):
            srcFolder = srcFolder.replace("**", "")
            path_encrypted = targetFolder + os.path.relpath(file, srcFolder)
            print(subprocess.check_output(['gpg', '--yes', '--verbose', '--output', path_encrypted + '.gpg', '--encrypt', '--recipient', recipient, file]))
