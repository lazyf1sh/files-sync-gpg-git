import unittest
import glob
from src import sync

def fun(x):
    return x + 1


class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)
    def test2(self):
        file = glob.glob("test_data/file_for_test_md5", recursive=True)
        self.assertEqual(sync.md5(file[0]), "de9e8b4b671fed9da2518ce488dbc138")