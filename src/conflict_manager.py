from src import sync


def calculateMovings(previous_remote_state, current_remote_state, previous_local_state, current_local_state):
    encrypt_to_right_no_conflicts = {}
    decrypt_to_left_no_conflicts = {}

    encrypt_to_right_rename_left = {}
    decrypt_to_left_rename_right = {}

    delete_on_left_no_conflicts = {}
    delete_on_right_no_conflicts = {}

    remote_elements_added = sync.find_added_elements_by_key(current_remote_state, previous_remote_state)
    remote_elements_modified = sync.find_modified_files(current_remote_state, previous_remote_state)
    remote_elements_removed = sync.find_removed_elements_by_key(current_remote_state, previous_remote_state)
    remote_elements_not_modified = {}

    local_elements_added = sync.find_added_elements_by_key(current_local_state, previous_local_state)
    local_elements_modified = sync.find_modified_files(current_local_state, previous_local_state)
    local_elements_removed = sync.find_removed_elements_by_key(current_local_state, previous_local_state)
    local_elements_not_modified = {}

    # operations calculations

    decrypt_to_left_no_conflicts.update(sync.find_added_elements_by_key(remote_elements_added, current_local_state))
    decrypt_to_left_no_conflicts.update(sync.find_added_elements_by_key(remote_elements_modified, current_local_state))
