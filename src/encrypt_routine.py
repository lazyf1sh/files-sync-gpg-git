import configparser
import logging
import subprocess
import os

config = configparser.ConfigParser()
config.read('default.conf')

recipient = config["default"]["gpg-recipient"]

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def encrypt_single_file(src_path, target_path):
    if os.path.isfile(src_path):
        output = subprocess.check_output(['gpg', '--yes', '--verbose', '--output', target_path, '--encrypt', '--recipient', recipient, src_path])
        logger.info(output)
    else:
        logger.info(src_path + " - is not a file")
