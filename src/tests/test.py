import glob
import unittest

from src.script import sync, utils


class RootUnitTest(unittest.TestCase):
    def test(self):
        self.assertEqual(4, 4)

    def test_sync_md5(self):
        file = glob.glob("test_data/file_for_test_md5", recursive=True)

        data_bytes = None
        with open('test_data/file_for_test_md5', 'rb') as myfile:
            data_bytes = myfile.read()
        md5_from_bytes = utils.md5_from_bytes(data_bytes)

        data_str = None
        with open('test_data/file_for_test_md5', 'r') as myfile:
            data_str = myfile.read()
        md5_from_string = utils.md5_from_string(data_str)

        self.assertEqual(utils.md5(file[0]), "de9e8b4b671fed9da2518ce488dbc138")
        self.assertEqual(md5_from_string, "de9e8b4b671fed9da2518ce488dbc138")
        self.assertEqual(md5_from_bytes, "de9e8b4b671fed9da2518ce488dbc138")

    def test_sync_build_md5_files_map_virtual(self):
        folder_src = "test_data/example-notes01/**"
        list_files = file = glob.glob(folder_src, recursive=True)
        result = sync.build_md5_files_map_virtual(list_files, folder_src)

        result_expected = {'/my note.md': '077f45c710cb114dac8b4c616ff90b02',
                           '/my catalog/': '694bedbaafb54cb2bd8e77446de20bf2',
                           '/my catalog/моя_zаметка.md': '641df979c3c529859c9057c122377290',
                           '/мой каталог/': 'f5da7a93453d475885d3a6eb7e38e8c6',
                           '/мой каталог/моя заметка.md': '67e6513b2f7ce9bac6bf8f67d8ed732c',
                           '/1.txt': '202cb962ac59075b964b07152d234b70'}
        self.assertDictEqual(result, result_expected)

    def test_find_modified_files(self):
        folder_local_previous = "test_data/example-notes03/local/local_previous"
        folder_local_current = "test_data/example-notes03/local/local_current"

        local_state_current = sync.calculate_state(folder_local_current)
        local_state_previous = sync.calculate_state(folder_local_previous)

        result = sync.find_modified_files(local_state_current, local_state_previous)
        result_expected = {'/local_modified2.txt': 'fc3972bc227d5542bfb378840cc617a1', '/local_modified1.txt': 'fc3972bc227d5542bfb378840cc617a1'}
        self.assertDictEqual(result, result_expected)

    def test_find_not_modified_files(self):
        folder_local_previous = "test_data/example-notes03/local/local_previous"
        folder_local_current = "test_data/example-notes03/local/local_current"

        local_state_current = sync.calculate_state(folder_local_current)
        local_state_previous = sync.calculate_state(folder_local_previous)

        result = sync.find_not_modified_files(local_state_current, local_state_previous)
        result_expected = {'/local_not_modified1.txt': '165a5d4656780db9bac7e5d1a6a73db5', '/local_not_modified2.txt': '165a5d4656780db9bac7e5d1a6a73db5'}
        self.assertDictEqual(result, result_expected)

    def test_compare_md5(self):
        file = "test_data/example-notes04/1.txt"
        md5_file = utils.md5(file)
        md5_string = utils.md5_from_string("123asd")
        self.assertEqual(md5_file, md5_string)

    def test_md5_from_bytes(self):
        bts = bytes([0x13, 0x00, 0x00, 0x00, 0x08, 0x01])
        bts_md5 = utils.md5_from_bytes(bts)

    def test_md5_from_bytes_None(self):
        bts_md5 = utils.md5_from_bytes(None)
        self.assertEqual(bts_md5, None)

    def test_path_leaf(self):
        paths = ['a/b/c/', 'a/b/c', '\\a\\b\\c', '\\a\\b\\c\\', 'a\\b\\c', 'a/b/../../a/b/c/', 'a/b/../../a/b/c', 'C:\\1\\1563602959_3/c', 'C:\\1\\1563602959_3/c/']
        for path in paths:
            leaf = utils.calc_path_leaf(path)
            self.assertEqual(leaf, 'c')

    def test_append_ts_to_path(self):
        current_ts = utils.get_current_unix_ts()
        paths = ['a/b/c/', 'a/b/c', '\\a\\b\\c', '\\a\\b\\c\\', 'a\\b\\c', 'a/b/../../a/b/c/', 'a/b/../../a/b/c', 'C:\\1\\1563602959_3/c', 'C:\\1\\1563602959_3/c/']
        for path in paths:
            leaf = utils.append_ts_to_path(path, current_ts)
