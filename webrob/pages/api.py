from flask import jsonify, request, session, redirect, render_template
from flask_login import current_user
from flask_user import login_required
import time
from urlparse import urlparse
from webrob.app_and_db import app, db
from webrob.docker import docker_interface
from webrob.docker.docker_interface import generate_mac
from webrob.models.users import User
from webrob.utility.random_string_builder import random_string
from webrob.config.settings import ROS_DISTRIBUTION

__author__ = 'mhorst@cs.uni-bremen.de'


@app.route('/api/v1.0/auth_by_session', methods=['GET'])
def login_by_session():
    """
    Returns authentication information for the currently logged in user as required by the knowrob.js authentication
    request
    """
    ip = docker_interface.get_container_ip(session['user_container_name'])
    return __generate_rosauth(session['user_container_name'], ip, True)


@app.route('/api/v1.0/refresh_by_session', methods=['GET'])
def refresh_by_session():
    """
    Refreshes the running session for a currently logged in user. This prevents a users container from being terminated
    automatically.
    """
    docker_interface.refresh(session['user_container_name'])
    return jsonify({'result': 'success'})


@app.route('/api/v1.0/ensure_started_by_session')
def ensure_started():
    """
    Tests if the container for the currently logged in user is running, and starts it if necessary.
    """
    if 'user_container_name' not in session:
        return False

    if not docker_interface.container_started(session['user_container_name']):
        __start_by_session()
    return jsonify(result=None)


@app.route('/api/v1.0/reset_by_session', methods=['POST'])
def reset_container():
    """
    Terminates and restarts the container for the currently logged in user.
    """
    if 'user_container_name' not in session:
        return False

    container_name = session['user_container_name']
    if docker_interface.container_started(container_name):
        docker_interface.stop_container(container_name)
    __start_by_session()
    return jsonify(result=None)


def __start_by_session():
    """
    Starts the container for the currently logged in user.
    """
    if 'user_container_name' not in session:
        return False
    image_name = __generate_user_image_name()
    container_name = session['user_container_name']
    docker_interface.start_user_container(image_name, container_name, ROS_DISTRIBUTION)


@app.route('/api/v1.0/auth_by_token/<string:token>', methods=['GET'])
def login_by_token(token):
    """
    Returns authentication information for the user assigned to the given API token. This is needed to authenticate
    against the rosbridge by third party clients.
    """
    user = __user_by_token(token)
    if user is None:
        return jsonify({'error': 'wrong api token'})
    ip = docker_interface.get_container_ip(user.username)
    return __generate_rosauth(user.username, ip)


@app.route('/api/v1.0/start_container/<string:token>', methods=['GET'])
def start_container(token):
    """
    Starts the container of the user assigned to the given API token. The WebSocket url to the users rosbridge instance
    will be returned on success.
    """
    user = __user_by_token(token)
    if user is None:
        return jsonify({'error': 'wrong api token'})

    docker_interface.start_user_container(__generate_user_image_name(), user.username, ROS_DISTRIBUTION)
    host_url = urlparse(request.host_url).hostname
    return jsonify({'result': 'success',
                    'url': '//' + host_url + '/ws/' + user.username + '/'})


@app.route('/api/v1.0/stop_container/<string:token>', methods=['GET'])
def stop_container(token):
    """
    Stops the container of the user assigned to the given API token.
    """
    user = __user_by_token(token)
    if user is None:
        return jsonify({'error': 'wrong api token'})
    docker_interface.stop_container(user.username)
    return jsonify({'result': 'success'})


@app.route('/api/v1.0/refresh_by_token/<string:token>', methods=['GET'])
def refresh_by_token(token):
    """
    Refreshes the running session for the user assigned to the given API token. This prevents a users container from
    being terminated automatically.
    """
    user = __user_by_token(token)
    if user is None:
        return jsonify({'error': 'wrong api token'})
    # TODO: Why is the main functionality commented out...?
    # docker_interface.refresh(user.username)
    return jsonify({'result': 'success'})


@app.route('/create_api_token', methods=['GET'])
@login_required
def create_api_token():
    __create_token()
    return render_template('show_user_data.html', **locals())


def __create_token():
    current_user.api_token = random_string(64)
    db.session.commit()
    session['api_token'] = current_user.api_token


def __user_by_token(token):
    """
    Returns the user object for the given API token, or None if no matching user could be found.
    """
    return User.query.filter_by(api_token=token).first()


def __generate_user_image_name():
    """
    Returns the image name to be used for user containers
    """
    return 'openease/' + ROS_DISTRIBUTION + '-knowrob-daemon'


def __generate_rosauth(user_container_name, dest, cache=False):
    """
    Generate the mac for use with rosauth and compile a json object with all necessary information to authenticate
    with the server.
    :param user_container_name: Name of the user container
    :param dest: IP of the destination
    :return: a json object for ros
    """
    client = request.remote_addr

    rand = random_string(30)

    t = int(time.time())
    level = "user"
    end = int(t + 3600)

    return jsonify({
        'mac': generate_mac(user_container_name, client, dest, rand, t, level, end, cache),
        'client': client,
        'dest': dest,
        'rand': rand,
        't': t,
        'level': level,
        'end': end
    })
