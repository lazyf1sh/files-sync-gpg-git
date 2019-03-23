from enum import Enum


class RenameStrategy(Enum):
    DO_NOTHING = 1
    DELETE_LOCAL = 2
    DELETE_LOCAL_RENAME_REMOTE = 3
    DELETE_BOTH = 4
    RENAME_REMOTE = 5
    RENAME_LOCAL = 6
    RENAME_LOCAL_DELETE_REMOTE = 7

