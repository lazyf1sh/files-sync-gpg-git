import tempfile
import unittest

from src.script import proc_runner


class RootUnitTest(unittest.TestCase):
    def test_1(self):
        working_dir = 'C:\\1\\files-sync-dev-sandbox-enviroment\PC1\encrypted'
        git_command = ['git', 'show', 'f6e2e2d414e98e73605c56c31f62f16df9db3b67:audacity.exe.gpg']
        args_bytes = proc_runner.execute_command_args_bytes(git_command, working_dir)
        print(args_bytes)
        self.assertTrue(True)

    def test_piped_linux(self):
        ls = ['ls', ]
        grep = ['grep', 'py']
        file_contents = proc_runner.run_piped(tempfile.gettempdir(), ls, grep)
        print(file_contents)
        self.assertTrue(True)
