from src import sync, RenameStrategy

def do_resolve(previous_remote_state, current_remote_state, previous_local_state, current_local_state):
    encrypt_to_right_no_conflicts = {}
    decrypt_to_left_no_conflicts = {}

    encrypt_to_right_rename_left = {}
    decrypt_to_left_rename_right = {}

    delete_on_left = {}
    delete_on_right = {}

    remote_elements_added = sync.find_added_elements_by_key(current_remote_state, previous_remote_state)
    remote_elements_removed = sync.find_removed_elements_by_key(current_remote_state, previous_remote_state)
    remote_elements_modified = sync.find_modified_files(current_remote_state, previous_remote_state)

    local_elements_added = sync.find_added_elements_by_key(current_local_state, previous_local_state)
    local_elements_removed = sync.find_removed_elements_by_key(current_local_state, previous_local_state)
    local_elements_modified = sync.find_modified_files(current_local_state, previous_local_state)

    sync.find_added_elements_by_key(remote_elements_added, local_elements_added)
    sync.find_intersection_by_keys(remote_elements_added, local_elements_added)

    copy_to_left = sync.find_added_elements_by_key(remote_elements_added, current_local_state)
    copy_to_left_with_timestamp = sync.find_added_elements_by_key(temp_right, local_elements_removed)

