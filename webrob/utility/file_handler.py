import os

def read_file(path):
    src_f = open(path, 'r')
    file = src_f.read()
    src_f.close()
    return file


def write_file(path, content):
    dst_f = open(path, 'w')
    dst_f.write(content)
    dst_f.close()


def create_file(path, content=None):
    dst_f = open(path, 'w+')
    if content != None:
        dst_f.write(content)
    dst_f.close()


def remove_file(path):
    os.remove(path)
