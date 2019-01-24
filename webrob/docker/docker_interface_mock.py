import base64
import hashlib
import os
import shutil
from urllib2 import URLError
import pyjsonrpc

from flask import flash, session
from pyjsonrpc.rpcerror import JsonRpcError
from webrob.app_and_db import app
from webrob.utility import random_string

def generate_mac(user_container_name, client_name, dest, rand, t, level, end, cache=False):
    """
    Generate the mac for use with rosauth. Choose params according to rosauth specification.
    """
    if cache and 'secret_t' in session and session['secret_t'] > t:
        secret = session['secret_key']
    else:
        secret = 'some_secret'
        if cache:
            session['secret_t'] = t + 60
            session['secret_key'] = secret
    return hashlib.sha512(secret + client_name + dest + rand + str(t) + level + str(end)).hexdigest()


def clear_secretcache():
    print('clear_secretcache')


def get_application_image_names():
    print('get_application_image_names')
    return {}


def get_webapp_image_names():
    print('get_webapp_image_names')
    return {}


def start_user_container(application_image, user_container_name, ros_distribution):
    print('start_user_container')


def start_webapp_container(webapp_image):
    print('start_webapp_container')


def stop_container(user_container_name):
    print('start_webapp_container')


def container_started(user_container_name, base_image=None):
    return True


def get_container_ip(user_container_name):
    print('get_application_image_names')
    return '0.0.0.0'


def get_container_log(user_container_name):
    print('get_container_log')
    return ''


def get_container_env(user_container_name, key):
    print('get_container_env')
    return ''


def refresh(user_container_name):
    print('refresh')

def file_exists(user_container_name, file):
    print('file_exists')
    return False


def file_rm(user_container_name, file, recursive=False):
    print('file_rm')


def file_ls(user_container_name, dir, recursive=False):
    print('file_ls')
    return {}


def file_read(user_container_name, file):
    print('file_read')
    return ''


def file_write(user_container_name, data, file):
    print('file_write')

# TODO: HACKY REFACTOR :(
class LFTransfer(object):
    """
    This class can be used in a with statement ( with LFTransfer() as lft: ) to copy large files/directories from/to
    the data container associated to the given container. The lft_data data container needs to be mounted inside the
    executing container beforehand. On initialization, a directory is created inside the lft_data container, where
    files can be placed for copying, or files can be copied to from the users data container. After the with-block ends,
    the directory inside the lft_data container is automatically removed.

    Example for copying data to the users container:
        with LFTransfer('user123') as lft:
            filename = os.path.join(lft.get_filetransfer_folder(), "large.file")
            f = open(filename, 'w')
            f.write("test")
            f.close()
            lft.to_container(filename, filename)

    Example for copying data from the users container:
        content = ''
        with LFTransfer('user123') as lft:
            filename = "my_experiment/owl/test.owl"
            lft.to_container(filename, filename)
            lft_path = os.path.join(lft.get_filetransfer_folder(), filename)
            f = open(lft_path, 'w')
            content = f.read()
            f.close()
    """
    def __init__(self, user_container):
        self.lftdir = None

    def get_filetransfer_folder(self):
        return self.lftdir

    def to_container(self, sourcefile, targetfile):
        if '/tmp/openEASE/dockerbridge' in sourcefile:
            source = os.path.relpath(sourcefile, '/tmp/openEASE/dockerbridge')
        elif self.lftdir not in sourcefile:
            source = os.path.relpath(os.path.join(self.lftdir, sourcefile), '/tmp/openEASE/dockerbridge')
        else:
            source = sourcefile

    def from_container(self, sourcefile, targetfile):
        if '/tmp/openEASE/dockerbridge' in targetfile:
            target = os.path.relpath(targetfile, '/tmp/openEASE/dockerbridge')
        elif self.lftdir not in targetfile:
            target = os.path.relpath(os.path.join(self.lftdir, targetfile), '/tmp/openEASE/dockerbridge')
        else:
            target = targetfile

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        shutil.rmtree(self.lftdir, True)