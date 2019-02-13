from webrob.utility.dir_name_getter import get_parent_dir_name
from webrob.utility.directory_handler import make_dirs
from webrob.utility.file_handler import read_file, create_file
from webrob.utility.path_exists_checker import exists as path_exists


def copy_template_file(src, dst, args):
    template = read_file(src)
    create_parent_dir(dst)
    copy_file_and_replace_keywords(dst, template, args)


def create_parent_dir(dst):
    parent = get_parent_dir_name(dst)
    if not path_exists(parent):
        make_dirs(parent)


def copy_file_and_replace_keywords(dst, template, args):
    create_file(dst, template.format(*args))
