from flask import session, request, redirect, url_for, render_template
from flask.ext.user.signals import user_logged_in
from flask.ext.user.signals import user_logged_out
from flask_user import current_user

from urlparse import urlparse

from random import choice
from string import lowercase

from webrob.app_and_db import app
from webrob.docker import docker_interface


@user_logged_in.connect_via(app)
def track_login(sender, user, **extra):
    app.logger.info("Logged in " + str(user.username))
    session['user_container_name'] = user.username
    session['username'] = user.username
    session['api_token'] = user.api_token


@user_logged_out.connect_via(app)
def track_logout(sender, user, **extra):
    if 'user_container_name' in session:
        docker_interface.stop_container(session['user_container_name'])
        session.pop('user_container_name')


@app.route('/')
def show_user_data():
    # if not current_user.is_authenticated:
    #    return redirect(url_for('user.login'))
    if 'user_container_name' not in session:
        # return redirect(url_for('user.logout'))
        # FIXME: delete knowrob container when user leaves the site
        __add_random_username_and_container_name_to_session()

    error = ""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = session['user_container_name']
    role_names = __get_user_roles()

    category = __get_exp_category()
    exp = __get_exp_name()

    # TODO: show_user_data never shown, could be re-enabled as iframe
    return render_template('main.html', **locals())
    # return render_template('show_user_data.html', **locals())


def __add_random_username_and_container_name_to_session():
    random_name = ''.join(choice(lowercase) for i in range(10))
    session['user_container_name'] = random_name
    session['username'] = random_name


def __get_user_roles():
    role_names = []
    if hasattr(current_user, 'roles'):
        role_names = map(lambda x: str(x.name), current_user.roles)
    return role_names


def __get_exp_category():
    if 'exp-category' in session:
        return session['exp-category']
    else:
        return None


def __get_exp_name():
    if 'exp-name' in session:
        return session['exp-name']
    else:
        return None


# Special route for EASE reviewers
@app.route('/ease-review')
def ease_review():
    session['exp-category'] = 'Pick-and-Place'
    session['exp-name'] = 'pr2-general-pick-and-place_0'
    return redirect('/')


@app.route('/remote')
def openease_remote():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    if 'user_container_name' not in session:
        return redirect(url_for('user.logout'))

    error = ""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = 'remote/172.17.42.1'
    role_names = __get_user_roles()

    category = __get_exp_category()
    exp = __get_exp_name()

    # TODO: show_user_data never shown, could be re-enabled as iframe
    return render_template('main.html', **locals())
