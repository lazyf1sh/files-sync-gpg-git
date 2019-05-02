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
    remote_elements_not_modified = sync.find_not_modified_files(current_remote_state, previous_remote_state)

    local_elements_added = sync.find_added_elements_by_key(current_local_state, previous_local_state)
    local_elements_modified = sync.find_modified_files(current_local_state, previous_local_state)
    local_elements_removed = sync.find_removed_elements_by_key(current_local_state, previous_local_state)
    local_elements_not_modified = sync.find_not_modified_files(current_local_state, previous_local_state)

    # operations calculations

    decrypt_to_left_no_conflicts.update(sync.find_added_elements_by_key(current_remote_state, current_local_state))
    decrypt_to_left_no_conflicts.update(sync.find_added_elements_by_key(remote_elements_modified, current_local_state))

    return decrypt_to_left_no_conflicts

def decrypt_to_left_no_conflicts(remote_state_previous, remote_state_current, local_state_previous, local_state_current):
    decrypt_to_left_no_conflicts = {}

    remote_elements_added = sync.find_added_elements_by_key(remote_state_current, remote_state_previous)
    remote_elements_modified = sync.find_modified_files(remote_state_current, remote_state_previous)
    remote_elements_removed = sync.find_removed_elements_by_key(remote_state_current, remote_state_previous)
    remote_elements_not_modified = sync.find_not_modified_files(remote_state_current, remote_state_previous)

    # operations calculations

    decrypt_to_left_no_conflicts.update(sync.find_added_elements_by_key(remote_state_current, local_state_current))

    return decrypt_to_left_no_conflicts


def on_left_to_trash_bin(previous_remote_state, current_remote_state, previous_local_state, current_local_state):
    remote_elements_removed = sync.find_removed_elements_by_key(current_remote_state, current_local_state)

    return remote_elements_removed

def on_right_remove(previous_remote_state, current_remote_state, previous_local_state, current_local_state):
    local_elements_removed = sync.find_removed_elements_by_key(current_local_state, current_remote_state)

    return local_elements_removed
