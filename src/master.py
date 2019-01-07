import glob
import sys
import os
import sync
import utils
import encrypt
import logging



folder_src = "./unencrypted/**" # use glob format
state_file = "previous_state.json";


files_unencrypted = glob.glob(folder_src, recursive=True)

current_state = sync.buildMd5FilesMapVirtual(files_unencrypted)
previous_state = utils.readJsonDictFromFile(state_file)

if previous_state == current_state:
    print("state is not changed")
    sys.exit(0)

elements_added = sync.findAddedElementsByKey(current_state, previous_state)
elements_removed = sync.findRemovedElementsByKey(current_state, previous_state)
elements_modified = sync.findModifiedFiles(current_state, previous_state)

utils.create_enc_dir_structure(elements_added.keys())
encrypt.encrypt_files(elements_added.keys())
utils.removeFiles(elements_removed.keys())
encrypt.encrypt_files(elements_modified.keys())


encrypt.gitcommitAndPush()

utils.dictToJson(state_file, current_state)

print("end")