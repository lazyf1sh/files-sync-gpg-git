import json


def readJsonDictFromFile(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
        return data


def dictToJson(filename, my_dict):
    with open(filename, 'w') as file:
        json.dump(my_dict, file, indent=4, sort_keys=True)