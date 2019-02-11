import os
import shutil


def mk_dir(path):
    os.mkdir(path)


def make_dirs(path):
    os.makedirs(path)


def rm_empty_dir(path):
    os.rmdir(path)


def rm_nonempty_dir(path):
    shutil.rmtree(path)
