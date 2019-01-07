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


def gitcommitAndPush():
    previous_cwd = os.getcwd()
    os.chdir("encrypted")
    executeCommand('git add *.gpg')
    executeCommand('git commit -m upd')
    os.chdir(previous_cwd)


def encrypt_files(files_enencrypted):
    for file in files_enencrypted:
        if os.path.isfile(file) and not file.lower().endswith('.gpg'):
                path_unencrypted = os.path.relpath(file)
                path_encrypted = 'encrypted/' + os.path.relpath(file, 'unencrypted')
                print(subprocess.check_output(['gpg', '--yes', '--verbose', '--output', path_encrypted + '.gpg', '--encrypt', '--recipient', recipient, path_unencrypted]))
