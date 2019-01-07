import json
import os

def readJsonDictFromFile(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
        return data


def dictToJson(filename, my_dict):
    with open(filename, 'w') as file:
        json.dump(my_dict, file, indent=4, sort_keys=True)


def create_targetDir(targetDir):
    if not os.path.exists(targetDir):
        try:
            os.makedirs(targetDir)
        except FileExistsError as e:
            print(e)



def create_enc_dir_structure(files_enencrypted, srcFolder, targetFolder):
    for file in files_enencrypted:
        if os.path.isdir(file):
            srcFolder = srcFolder.replace("**", "")
            path_encrypted = targetFolder + os.path.relpath(file, srcFolder)
            if path_encrypted.find(".") == 0:
                continue
            else:
                if not os.path.exists(path_encrypted):
                    os.makedirs(path_encrypted)

def removeFiles(paths, srcFolder, targetFolder):
    for path in paths:
        srcFolder = srcFolder.replace("**", "")
        encrypted_path = targetFolder + os.path.relpath(path, srcFolder) + ".gpg"
        if os.path.exists(encrypted_path) and os.path.isfile(encrypted_path):
            os.remove(encrypted_path)