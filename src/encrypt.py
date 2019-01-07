import csv
import glob
import hashlib
import json
import os
import subprocess
import shlex
import pickle
import pprint



toCommit = []



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
    os.chdir('encrypted')
    executeCommand('git add *.gpg')
    executeCommand('git commit -m upd')


def encrypt_files():
    for file in files_enencrypted:
        path_unencrypted = os.path.relpath(file)
        path_encrypted = 'encrypted/' + os.path.relpath(file, 'unencrypted')
        if os.path.isfile(file) and not file.lower().endswith('.gpg'):
            print(subprocess.check_output(['gpg', '--yes', '--verbose', '--output', path_encrypted + '.gpg', '--encrypt', '--recipient', 'stealthwar@gmail.com', path_unencrypted]))


def create_enc_dir_structure():
    for file in files_enencrypted:
        path_encrypted = 'encrypted/' + os.path.relpath(file, 'unencrypted')
        if os.path.isdir(file) and file.find("encrypted/"):
            if path_encrypted.find(".") == 0:
                continue
            else:
                if not os.path.exists(path_encrypted):
                    os.makedirs(path_encrypted)

# fromFileMd5 = readMd5sFromFile()
# virtualFileMd5 = buildMd5FilesMapVirtual()
# addMd5sToFile(virtualFileMd5)
# create_enc_dir_structure()
# encrypt_files()
# gitcommitAndPush()
