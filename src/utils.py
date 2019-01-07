import json
import os

def readJsonDictFromFile(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
        return data


def dictToJson(filename, my_dict):
    with open(filename, 'w') as file:
        json.dump(my_dict, file, indent=4, sort_keys=True)


def create_enc_dir_structure(files_enencrypted):
    try:
        os.makedirs("encrypted/")
    except FileExistsError as e:
        print(e)

    for file in files_enencrypted:
        if os.path.isdir(file) and file.find("encrypted/"):
            path_encrypted = 'encrypted/' + os.path.relpath(file, 'unencrypted')
            if path_encrypted.find(".") == 0:
                continue
            else:
                if not os.path.exists(path_encrypted):
                    os.makedirs(path_encrypted)