import logging
import os
import shlex
import subprocess
import sys
from subprocess import Popen

logger = logging.getLogger(__name__)


def run_piped(working_dir, args1, args2):
    logger.info("running piped command")
    logger.info("executing command 1: %s | working dir: %s", args1, working_dir)
    logger.info("executing command 2: %s | working dir: %s", args2, working_dir)
    previous_working_dir = os.getcwd()
    try:
        os.chdir(working_dir)
        p1 = Popen(args1, stdout=subprocess.PIPE)
        p2 = Popen(args2, stdin=p1.stdout, stdout=subprocess.PIPE)

        out, err = p2.communicate()

        p1.stdout.close()
        p2.stdout.close()

        return out
    except Exception as exc:
        logger.critical("Critical error. Exception: %s", str(exc))
        raise exc
    finally:
        os.chdir(previous_working_dir)


def execute_command_args_bytes(args, working_dir):
    return execute_command_internal(args, working_dir)


def execute_command_internal(args, working_dir):
    """

    :param args:
    :param working_dir:
    :return: bytes
    """
    logger.debug("executing command: %s | working dir: %s", args, working_dir)
    previous_working_dir = os.getcwd()
    os.chdir(working_dir)
    try:
        proc = subprocess.check_output(args)
        # logger.debug("Command executed: %s\nExec result: %s\n", args, proc)
        return proc
    except subprocess.CalledProcessError as exc:
        logger.critical("Critical error: Code: %s", exc.returncode)
        logger.critical("Critical error. Exception: %s", str(exc))
        raise exc
    finally:
        os.chdir(previous_working_dir)


def execute_command_args(args, working_dir) -> str:
    my_bytes = execute_command_internal(args, working_dir)
    try:
        return my_bytes.decode("UTF-8")
    except Exception as e:
        logger.warning(e)
        return str(my_bytes)


def execute_command_string(command, working_dir) -> str:
    args = shlex.split(command, posix="win" not in sys.platform)
    bytes1 = execute_command_internal(args, working_dir)
    try:
        return bytes1.decode("UTF-8")
    except Exception as e:
        logger.error(e)
        raise Exception("Error executing command")
