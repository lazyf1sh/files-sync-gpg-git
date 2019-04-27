import unittest
import glob
from src import sync, conflict_manager

def fun(x):
    return x + 1


class RootUnitTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)
    def test_sync_md5(self):
        file = glob.glob("test_data/file_for_test_md5", recursive=True)
        self.assertEqual(sync.md5(file[0]), "de9e8b4b671fed9da2518ce488dbc138")
    def test_sync_build_md5_files_map_virtual(self):
        folder_src = "test_data/example-notes01/**"
        list_files = file = glob.glob(folder_src, recursive=True)
        result = sync.build_md5_files_map_virtual(list_files, folder_src)

        result_expected = { '/my note.md': '077f45c710cb114dac8b4c616ff90b02',
                            '/my catalog/': '694bedbaafb54cb2bd8e77446de20bf2',
                            '/my catalog/моя_zаметка.md': '641df979c3c529859c9057c122377290',
                            '/мой каталог/': 'f5da7a93453d475885d3a6eb7e38e8c6',
                            '/мой каталог/моя заметка.md': '67e6513b2f7ce9bac6bf8f67d8ed732c',
                            '/1.txt':'202cb962ac59075b964b07152d234b70' }
        self.assertDictEqual(result, result_expected)
    def test_ewqudjsadlkaslkdjaslda(self):
        folder_remote_previous = "test_data/example-notes02/remote/remote_previous"
        folder_remote_current = "test_data/example-notes02/remote/remote_current"

        folder_local_previous = "test_data/example-notes02/local/local_previous"
        folder_local_current = "test_data/example-notes02/local/local_current"

        previous_remote_state = sync.calculate_state_without_gpg_ext(folder_remote_previous)
        current_remote_state = sync.calculate_state_without_gpg_ext(folder_remote_current)

        current_local_state = sync.calculate_state(folder_local_current)
        previous_local_state = sync.calculate_state(folder_local_previous)

        conflict_manager.calculateMovings(previous_remote_state, current_remote_state, previous_local_state, current_local_state)
    def test_find_modified_files(self):
            folder_local_previous = "test_data/example-notes03/local/local_previous"
            folder_local_current = "test_data/example-notes03/local/local_current"

            local_state_current = sync.calculate_state(folder_local_current)
            local_state_previous = sync.calculate_state(folder_local_previous)

            result = sync.find_modified_files(local_state_current, local_state_previous)
            result_expected = {'/local_modified.txt': '28b4c6c4bceb2ad7aa666b9d90143198'}
            self.assertDictEqual(result, result_expected)
    def test_find_not_modified_files(self):
            folder_local_previous = "test_data/example-notes03/local/local_previous"
            folder_local_current = "test_data/example-notes03/local/local_current"

            local_state_current = sync.calculate_state(folder_local_current)
            local_state_previous = sync.calculate_state(folder_local_previous)

            result = sync.find_not_modified_files(local_state_current, local_state_previous)
            result_expected = {'/local_not_modified.txt': '165a5d4656780db9bac7e5d1a6a73db5'}
            self.assertDictEqual(result, result_expected)
