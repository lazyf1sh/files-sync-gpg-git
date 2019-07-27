import configparser
import logging
import subprocess
import os

from src import utils

config = configparser.ConfigParser()
config.read('default.conf')

recipient = config["default"]["gpg-recipient"]

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def encrypt_single_file(src_path, target_path, working_dir):
    if os.path.isfile(src_path):
        logging.info("encrypting file: %s", src_path)
        output = utils.execute_command_args(['gpg', '--yes', '--verbose', '--output', target_path, '--encrypt', '--recipient', recipient, src_path], working_dir)
        logger.info("encrypted file: %s", output)
    else:
        logger.info(src_path + " - is not a file")
