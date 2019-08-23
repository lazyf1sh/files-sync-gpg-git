import logging
import os
import subprocess
from subprocess import Popen

logger = logging.getLogger(__name__)


def run_piped(working_dir, args1, args2):
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
