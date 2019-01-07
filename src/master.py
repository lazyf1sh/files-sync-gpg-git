import glob
from src import sync
from src import Utils

files_enencrypted = glob.glob("./unencrypted/**", recursive=True)
struct_md5 = {}

app_virtual_md5 = sync.buildMd5FilesMapVirtual(files_enencrypted)
struct_md5 = Utils.readJsonDictFromFile("struct_md5")
value = sync.findDiffByKey(app_virtual_md5, struct_md5)

print(value)
