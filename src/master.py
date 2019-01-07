import glob
import sys
import os
import sync
import utils
import encrypt
import logging
import configparser

config = configparser.ConfigParser()
config.read('default.conf')

folder_src = config["default"]["source-dir"]
folder_target = config["default"]["target-dir"]
state_file = "previous_state.json";


files_unencrypted = glob.glob(folder_src, recursive=True)

current_state = sync.buildMd5FilesMapVirtual(files_unencrypted)
previous_state = utils.readJsonDictFromFile(state_file)

if previous_state == current_state:
    print("state is not changed")
    print("end\n")
    sys.exit(0)

elements_added = sync.findAddedElementsByKey(current_state, previous_state)
elements_removed = sync.findRemovedElementsByKey(current_state, previous_state)
elements_modified = sync.findModifiedFiles(current_state, previous_state)


utils.create_targetDir(folder_target)
utils.create_enc_dir_structure(elements_added.keys(), folder_src, folder_target)
encrypt.encrypt_files(elements_added.keys(), folder_src, folder_target)
utils.removeFiles(elements_removed.keys(), folder_src, folder_target)
encrypt.encrypt_files(elements_modified.keys(), folder_src, folder_target)


encrypt.gitcommitAndPush(folder_target)

utils.dictToJson(state_file, current_state)

print("end\n")