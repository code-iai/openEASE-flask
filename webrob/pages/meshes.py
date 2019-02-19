__author__ = 'danielb@cs.uni-bremen.de'

import os
import sys
import traceback

from flask import send_from_directory, jsonify
from flask_user import login_required
from urllib import urlopen, urlretrieve
from subprocess import call
import thread

from webrob.app_and_db import app
from webrob.config.settings import MESH_REPOSITORIES
from webrob.utility.directory_handler import ch_dir
from webrob.utility.path_handler import join_paths, path_exists, get_parent_dir_name, get_path_basename, \
    get_unix_style_path_basename

ROS_MESH_DATA_DIR = '/home/ros/mesh_data'


def update_meshes():
    if path_exists(ROS_MESH_DATA_DIR):
        thread.start_new_thread(__update_meshes_run, ())


def __update_meshes_run():
    __change_to_mesh_data_directory()
    __update_mesh_repositories()
    __convert_tif_images_to_png()


def __change_to_mesh_data_directory():
    ch_dir(ROS_MESH_DATA_DIR)


def __update_mesh_repositories():
    for repo in MESH_REPOSITORIES:
        __update_if_svn_or_git_repository(repo)


def __update_if_svn_or_git_repository(repo):
    try:
        (tool, url) = repo
        if __tool_is_svn_repository(tool):
            __update_meshes_in_repository(url, "/usr/bin/svn", "update", "co")
        elif __tool_is_git_repository(tool):
            __update_meshes_in_repository(url, "/usr/bin/git", "pull", "clone")
    except Exception:
        app.logger.warn("Unable to update repository: '" + str(repo) + "'.")


def __tool_is_svn_repository(tool):
    return tool == "svn"


def __tool_is_git_repository(tool):
    return tool == "git"


def __update_meshes_in_repository(url, repo_dir, repo_update_cmd, repo_clone_cmd):
    repo_name = get_unix_style_path_basename(url)
    if __repository_exists(repo_name):
        __update_repository(repo_name, repo_dir, repo_update_cmd)
    else:
        __clone_repository(repo_dir, repo_clone_cmd, url)


def __repository_exists(repo_name):
    path_exists(repo_name)


def __update_repository(repo_name, repo_dir, repo_update_cmd):
    ch_dir(repo_name)
    call([repo_dir, repo_update_cmd])
    ch_dir('..')


def __clone_repository(repo_dir, repo_clone_cmd, url):
    call([repo_dir, repo_clone_cmd, url])


def __convert_tif_images_to_png():
    call(['/opt/webapp/convert-recursive', ROS_MESH_DATA_DIR])


@app.route('/meshes/<path:mesh>')
def download_mesh(mesh):
    mesh_file = __get_mesh_file(mesh)

    if mesh_file is None:
        __log_download_fail_message(mesh)
        return jsonify(result=None)

    return __send_mesh_file(mesh, mesh_file)


def __get_mesh_file(mesh):
    m_file = __get_m_file_from_repos(mesh)

    if m_file is None:
        m_file = __get_m_file_from_root(mesh)

    return m_file


def __get_m_file_from_repos(mesh):
    m_file = None

    for repo in os.listdir(ROS_MESH_DATA_DIR):
        repo_path = join_paths(ROS_MESH_DATA_DIR, repo)
        mesh_path = join_paths(repo_path, mesh)
        if path_exists(mesh_path):
            m_file = mesh_path

    return m_file


def __get_m_file_from_root(mesh):
    if path_exists(mesh):
        return mesh
    elif path_exists('/' + mesh):
        return '/' + mesh


def __log_download_fail_message(mesh):
    app.logger.info("Unable to download mesh " + mesh)


def __send_mesh_file(mesh_file):
    return send_from_directory(
        get_parent_dir_name(mesh_file),
        get_path_basename(mesh_file))


def is_mesh_url_valid(url):
    return urlopen(url).getcode() == 200
