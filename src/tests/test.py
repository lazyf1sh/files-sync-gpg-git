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


class MyTest2(unittest.TestCase):
    def test(self):
        folder_src = "test_data/example-notes/**"
        list_files = file = glob.glob(folder_src, recursive=True)
        result = sync.build_md5_files_map_virtual(list_files, folder_src)

        result_expected = { '/my note.md': '077f45c710cb114dac8b4c616ff90b02',
                            '/my catalog/': '694bedbaafb54cb2bd8e77446de20bf2',
                            '/my catalog/моя_zаметка.md': '641df979c3c529859c9057c122377290',
                            '/мой каталог/': 'f5da7a93453d475885d3a6eb7e38e8c6',
                            '/мой каталог/моя заметка.md': '67e6513b2f7ce9bac6bf8f67d8ed732c',
                            '/1.txt':'202cb962ac59075b964b07152d234b70' }
        self.assertDictEqual(result, result_expected)
        self