from src import sync, RenameStrategy

def get_to_rename_locally(remote_elements_added, remote_elements_modified, current_local_state):
    to_merge_conflicts_locally = {}
    to_merge_conflicts_locally.update(sync.find_intersection_by_keys(remote_elements_added, current_local_state))
    to_merge_conflicts_locally.update(sync.find_intersection_by_keys(remote_elements_modified, current_local_state))
    var = RenameStrategy.RenameStrategy.DELETE_BOTH




