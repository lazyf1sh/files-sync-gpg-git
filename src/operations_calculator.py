from src import sync


def calculateMovings2(previous_remote_state, current_remote_state, previous_local_state, current_local_state):
    to_check_conflict_and_rename_right = {}

    remote_elements_added = sync.find_added_elements_by_key(current_remote_state, previous_remote_state)
    remote_elements_modified = sync.find_modified_files(current_remote_state, previous_remote_state)
    remote_elements_removed = sync.find_removed_elements_by_key(current_remote_state, previous_remote_state)
    remote_elements_not_modified = sync.find_not_modified_files(current_remote_state, previous_remote_state)

    local_elements_added = sync.find_added_elements_by_key(current_local_state, previous_local_state)
    local_elements_modified = sync.find_modified_files(current_local_state, previous_local_state)
    local_elements_removed = sync.find_removed_elements_by_key(current_local_state, previous_local_state)
    local_elements_not_modified = sync.find_not_modified_files(current_local_state, previous_local_state)

    return ""


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


def group_7(previous_remote_state, current_remote_state, previous_local_state, current_local_state):
    remote_elements_added = sync.find_added_elements_by_key(current_remote_state, previous_remote_state)
    remote_elements_modified = sync.find_modified_files(current_remote_state, previous_remote_state)
    remote_elements_not_modified = sync.find_not_modified_files(current_remote_state, previous_remote_state)

    local_elements_added = sync.find_added_elements_by_key(current_local_state, previous_local_state)
    local_elements_modified = sync.find_modified_files(current_local_state, previous_local_state)
    local_elements_not_modified = sync.find_not_modified_files(current_local_state, previous_local_state)

    result = {}
    result.update(sync.find_intersection_by_keys(local_elements_modified, remote_elements_not_modified))

    return result


def group_8(previous_remote_state, current_remote_state, previous_local_state, current_local_state):
    remote_elements_added = sync.find_added_elements_by_key(current_remote_state, previous_remote_state)
    remote_elements_modified = sync.find_modified_files(current_remote_state, previous_remote_state)
    remote_elements_not_modified = sync.find_not_modified_files(current_remote_state, previous_remote_state)

    local_elements_added = sync.find_added_elements_by_key(current_local_state, previous_local_state)
    local_elements_modified = sync.find_modified_files(current_local_state, previous_local_state)
    local_elements_not_modified = sync.find_not_modified_files(current_local_state, previous_local_state)

    result = {}
    result.update(sync.find_intersection_by_keys(local_elements_not_modified, remote_elements_modified))

    return result


def group_1(previous_remote_state, current_remote_state, previous_local_state, current_local_state):
    remote_elements_added = sync.find_added_elements_by_key(current_remote_state, previous_remote_state)
    remote_elements_modified = sync.find_modified_files(current_remote_state, previous_remote_state)
    remote_elements_not_modified = sync.find_not_modified_files(current_remote_state, previous_remote_state)

    local_elements_added = sync.find_added_elements_by_key(current_local_state, previous_local_state)
    local_elements_modified = sync.find_modified_files(current_local_state, previous_local_state)
    local_elements_not_modified = sync.find_not_modified_files(current_local_state, previous_local_state)

    result = {}
    result.update(sync.find_intersection_by_keys(local_elements_modified, remote_elements_added))
    result.update(sync.find_intersection_by_keys(local_elements_modified, remote_elements_modified))

    result.update(sync.find_intersection_by_keys(local_elements_not_modified, remote_elements_added))
    result.update(sync.find_intersection_by_keys(local_elements_not_modified, remote_elements_not_modified))

    result.update(sync.find_intersection_by_keys(local_elements_added, remote_elements_added))
    result.update(sync.find_intersection_by_keys(local_elements_added, remote_elements_modified))
    result.update(sync.find_intersection_by_keys(local_elements_added, remote_elements_not_modified))

    # result = sync.find_intersection_by_keys(current_local_state, current_remote_state)
    return result


def group_3(previous_remote_state, current_remote_state, previous_local_state, current_local_state):
    remote_elements_removed = sync.find_removed_elements_by_key(current_remote_state, previous_remote_state)
    result = sync.find_intersection_by_keys(remote_elements_removed, current_local_state)

    return result


def group_5(previous_remote_state, current_remote_state, previous_local_state, current_local_state):
    result = sync.find_added_elements_by_key(current_local_state, previous_remote_state)
    result = sync.find_added_elements_by_key(result, current_remote_state)  # to ensure
    return result


def group_6(previous_remote_state, current_remote_state, previous_local_state, current_local_state):
    result = sync.find_added_elements_by_key(current_remote_state, previous_local_state)
    result = sync.find_added_elements_by_key(result, current_local_state)  # to ensure

    return result


def group_2_4(previous_remote_state, current_remote_state, previous_local_state, current_local_state):
    # action group #2
    local_elements_removed = sync.find_removed_elements_by_key(current_local_state, previous_local_state)
    result = sync.find_intersection_by_keys(local_elements_removed, current_remote_state)

    return result
