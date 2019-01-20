import sys
from src import decrypt_logic, encrypt_logic, utils
import configparser

config = configparser.ConfigParser()
config.read('default.conf')

folder_unencrypted = config["default"]["dir-unencrypted"]
folder_encrypted = config["default"]["dir-encrypted"]
state_file = "previous_state.json"


if sys.argv[1] == "e" or sys.argv[1] == "enc" or sys.argv[1] == "encrypt":
    encrypt_logic.encrypt_run(folder_unencrypted, folder_encrypted, state_file)
    utils.stop_application()

if sys.argv[1] == "d" or sys.argv[1] == "dec" or sys.argv[1] == "decrypt":
    decrypt_logic.decrypt_run(folder_encrypted, folder_unencrypted)
    utils.stop_application()

print("No args provided. Use 'encrypt' or 'decrypt'.")
