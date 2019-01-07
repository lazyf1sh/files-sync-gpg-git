import hashlib
import os


def buildMd5FilesMapVirtual(list_files):
    result = {}
    for file in list_files:
        if os.path.isfile(file):
            filemd5 = md5(file)
            result[file] = filemd5
        if os.path.isdir(file):
            md5FromDirPath = md5FromString(file)
            result[file] = md5FromDirPath
    return result




def findDiffByKey(dict1, dict2):
    return {k: dict1[k] for k in set(dict1) - set(dict2)}

def findModifiedFiles(dict1, dict2):
    sameNames = findIntersectionByKeys(dict1, dict2) # files that have the same names but may be modified
    same1 = findIntersectionByKeys(dict1, sameNames)
    same2 = findIntersectionByKeys(dict2, sameNames)
    diff = set(same1.values()) - set(same2.values())
    swapped = {v: k for k, v in dict1.items()}
    result = {swapped[i]: i for i in diff}
    return result



def findIntersectionByKeys(dict1, dict2):
    return {k: dict1[k] for k in set(dict1).intersection(set(dict2))}


def findAddedElementsByKey(dict1, dict2):
    return findDiffByKey(dict1, dict2)

def findRemovedElementsByKey(dict1, dict2):
    return findDiffByKey(dict2, dict1)


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def md5FromString(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()