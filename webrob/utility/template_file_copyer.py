import os

from webrob.utility.file_handler import read_file, write_file

#TODO

def copy_template_file(src, dst, args):
    template = read_file(src)
    create_parent_dir(dst)
    copy_file_and_replace_keywords(dst, template, args)

def create_parent_dir(dst):
    parent = os.path.dirname(dst)
    if not os.path.exists(parent):  os.makedirs(parent)

def copy_file_and_replace_keywords(dst, template, args):
    write_file(dst, template % args)
