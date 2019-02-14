import os
import posixpath


def join_paths(path, *paths):
    return os.path.join(path, *paths)


def path_exists(path):
    return os.path.exists(path)


def absolute_path(path):
    return os.path.abspath(path)


def get_parent_dir_name(path):
    return os.path.dirname(path)


def get_path_basename(path):
    return os.path.basename(path)


def get_unix_style_path_basename(path):
    return posixpath.basename(path)
