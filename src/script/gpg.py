import configparser
import logging
import os
import subprocess
import sys

from src.script import utils

if len(sys.argv) < 2:
    print("missing arguments")
    sys.exit(1)

logger = logging.getLogger(__name__)

main_conf = sys.argv[1]

config = configparser.ConfigParser()
config.read(main_conf)

gpg_verbose = config["default"].getboolean('gpg-verbose')
recipient = config["default"]["gpg-recipient"]


def gpg_version(working_dir):
    try:
        args = ['gpg', '--version']
        output = subprocess.check_output(args)
        args_bytes = utils.execute_command_args(args, working_dir)
        gpg_lines = args_bytes.split("\n")

        if len(gpg_lines) > 1:
            logger.info(gpg_lines[0])
            return True
    except subprocess.CalledProcessError as e:
        logger.critical("error getting gpg version", e)
    return False


def decrypt_single_file(source_path, target_path):
    if os.path.isfile(source_path):
        if source_path.lower().endswith('.gpg'):
            try:
                args = ['gpg', '--yes', '--output', target_path]
                if gpg_verbose:
                    args.append('--verbose')
                args.append('--decrypt')
                args.append(source_path)

                output = subprocess.check_output(args)
                logger.debug(output)
            except subprocess.CalledProcessError as e:
                logger.critical("Error decrypting %s\n\nException: %s", source_path, e)
        else:
            logger.error("The file have no gpg extension. that is very strange situation, because in repo must be only .gpg-files: %s", source_path)
    else:
        logger.error("Please do filtering before calling. Path is not a file: %s", source_path)


def decrypt_single_file_inmemory(source_path, working_dir):
    """
    :param working_dir:
    :rtype: str
    :param source_path: source file path
    :return: file contents
    """
    if os.path.isfile(source_path):
        args = ['gpg', '--yes']
        if gpg_verbose:
            args.append('--verbose')
        args.append('--decrypt')
        args.append(source_path)
        args_bytes = utils.execute_command_args_bytes(args, working_dir)
        if args_bytes is None:
            logger.critical("None is received for %s", source_path)
        return args_bytes


def encrypt_single_file(src_path, target_path, working_dir):
    if os.path.isfile(src_path):
        logger.info("encrypting file: %s", src_path)

        args = ['gpg', '--yes']
        if gpg_verbose:
            args.append('--verbose')
        args.append('--output')
        args.append(target_path)
        args.append('--encrypt')
        args.append('--recipient')
        args.append(recipient)
        args.append(src_path)

        utils.execute_command_args_bytes(args, working_dir)
        logger.info("encrypted file: %s", src_path)
    else:
        logger.error("path is not a file: %s", src_path)
