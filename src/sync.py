import hashlib
import os


def buildMd5FilesMapVirtual(list_files):
    result = {}
    for file in list_files:
        if os.path.isfile(file):
            filemd5 = md5(file)
            result[file] = filemd5
    return result


def findDiffByKey(dict1, dict2):
    return {k: dict1[k] for k in set(dict1) - set(dict2)}


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
