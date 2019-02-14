import re

from webrob.utility.dir_name_getter import get_parent_dir_name
from webrob.utility.directory_handler import make_dirs
from webrob.utility.file_handler import read_file, create_file
from webrob.utility.path_handler import path_exists as path_exists


def copy_template_file(src, dst, args):
    template = read_file(src)
    __create_parent_dir(dst)
    __copy_file_and_replace_keywords(dst, template, args)


def __create_parent_dir(dst):
    parent = get_parent_dir_name(dst)
    if not path_exists(parent):
        make_dirs(parent)


def __copy_file_and_replace_keywords(dst, template, args):
    content = __format_template(template, args)
    create_file(dst, content)


def __format_template(template, args):
    if __get_number_of_template_fillers(template) < len(args):
        raise IndexError('number of arguments for str.format() is more than the number of fillers in the template')
    elif __get_number_of_template_fillers(template) > len(args):
        raise IndexError('number of arguments for str.format() is less than the number of fillers in the template')
    return template.format(*args)


def __get_number_of_template_fillers(template):
    # find all occurences of {[integer number]} in template
    string_matches = re.findall('({[0-9]+})', template)
    return len(string_matches)
