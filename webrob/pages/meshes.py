__author__ = 'danielb@cs.uni-bremen.de'

import os
import sys
import traceback

from flask import send_from_directory, jsonify
from flask_user import login_required
from urllib import urlopen, urlretrieve
from subprocess import call
from posixpath import basename
import thread

from webrob.app_and_db import app
from webrob.config.settings import MESH_REPOSITORIES


def is_mesh_url_valid(url):
    return urlopen(url).getcode() == 200


def update_meshes_run():
    os.chdir('/home/ros/mesh_data')
    for repo in MESH_REPOSITORIES:
        try:
            (tool, url) = repo
            if tool == "svn":
                update_meshes_svn(url)
            elif tool == "git":
                update_meshes_git(url)
        except Exception:
            app.logger.warn("Unable to update repository: '" + str(repo) + "'.")
    # Convert tif images to png images
    call(['/opt/webapp/convert-recursive', '/home/ros/mesh_data'])


def update_meshes():
    thread.start_new_thread(update_meshes_run, ())


def update_meshes_svn(url):
    repo_name = basename(url)
    if os.path.exists(repo_name):
        os.chdir(repo_name)
        call(["/usr/bin/svn", "update"])
        os.chdir('..')
    else:
        call(["/usr/bin/svn", "co", url])


def update_meshes_git(url):
    repo_name = basename(url)
    if os.path.exists(repo_name):
        os.chdir(repo_name)
        call(["/usr/bin/git", "pull"])
        os.chdir('..')
    else:
        call(["/usr/bin/git", "clone", url])


@app.route('/meshes/<path:mesh>')
def download_mesh(mesh):
    mesh_file = None
    for repo in os.listdir('/home/ros/mesh_data'):
        repo_path = os.path.join('/home/ros/mesh_data', repo)
        mesh_path = os.path.join(repo_path, mesh)
        if os.path.exists(mesh_path):
            mesh_file = mesh_path

    if mesh_file is None:
        if os.path.exists(mesh):
            mesh_file = mesh
        elif os.path.exists('/' + mesh):
            mesh_file = '/' + mesh

    if mesh_file is None:
        app.logger.info("Unable to download mesh " + mesh)
        return jsonify(result=None)

    return send_from_directory(
        os.path.dirname(mesh_file),
        os.path.basename(mesh_file))
