import os

from webrob.utility.path_handler import path_exists


def read_file(path):
    src_f = open(path, 'r')
    file = src_f.read()
    src_f.close()
    return file


def write_to_file(path, content):
    if path_exists(path) is False:
        raise IOError('File does not exist.')

    dst_f = open(path, 'w')
    dst_f.write(content)
    dst_f.close()


def create_file(path, content=None):
    if path_exists(path) is True:
        raise IOError('Files cannot be overwritten with this method.')

    dst_f = open(path, 'w+')
    if content is not None:
        dst_f.write(content)
    dst_f.close()


def remove_file(path):
    os.remove(path)
