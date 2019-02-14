import os


def join_paths(path, *paths):
    return os.path.join(path, *paths)


def path_exists(path):
    return os.path.exists(path)


def absolute_path(path):
    return os.path.abspath(path)
