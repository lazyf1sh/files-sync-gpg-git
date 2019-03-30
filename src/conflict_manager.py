from src import sync, RenameStrategy

def do_resolve(previous_remote_state, current_remote_state, previous_local_state, current_local_state):
    remote_elements_added = sync.find_added_elements_by_key(current_remote_state, previous_remote_state)
    remote_elements_removed = sync.find_removed_elements_by_key(current_remote_state, previous_remote_state)
    remote_elements_modified = sync.find_modified_files(current_remote_state, previous_remote_state)

    local_elements_added = sync.find_added_elements_by_key(current_local_state, previous_local_state)
    local_elements_removed = sync.find_removed_elements_by_key(current_local_state, previous_local_state)
    local_elements_modified = sync.find_modified_files(current_local_state, previous_local_state)

    temp = {}
    temp.update(remote_elements_added)
    temp.update(remote_elements_modified)

    copy_to_left = sync.find_added_elements_by_key(temp, current_local_state)

