import glob
from src import sync
from src import utils
from src import encrypt

folder_src = "./unencrypted/**" # use glob format

files_unencrypted = glob.glob(folder_src, recursive=True)

current_state = sync.buildMd5FilesMapVirtual(files_unencrypted)
previous_state = utils.readJsonDictFromFile("previous_state.json")

elements_added = sync.findAddedElementsByKey(current_state, previous_state)
elements_removed = sync.findRemovedElementsByKey(current_state, previous_state)
elements_modified = sync.findModifiedFiles(current_state, previous_state)

utils.create_enc_dir_structure(elements_added.keys())
encrypt.encrypt_files(elements_added.keys())


print("end")