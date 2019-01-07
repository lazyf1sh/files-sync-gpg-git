import shlex
import subprocess
import glob
import os

#files = glob.glob("/home/qwerty/sandbox-py/src/encrypted/**", recursive=True)


# for file in files:
#     if os.path.isfile(file) and file.lower().endswith('.gpg'):
#         args = shlex.split('gpg --output ' + file.replace('.gpg', '') + ' --verbose --decrypt ' + file)
#         print(subprocess.check_output(args))