#
# Based on https://github.com/lingthio/Flask-User-starter-app
# 
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from logging.handlers import SMTPHandler
import os
import datetime

import webrob.utility.environment_variable_getter as evg

from flask_mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter
from flask.ext.babel import Babel

from webrob.utility.random_string_builder import random_string
from webrob.startup.init_db import *
from webrob.startup.init_webapp import *
from webrob.models.users import Role, User

from werkzeug.security import generate_password_hash, check_password_hash


def add_user(app, db, user_manager, name, mail, pw, display_name='', remote_app='', roles=[]):
    if not __password_is_valid(app, name, pw):
        return

    user = __get_user_from_db(name)

    if not user:
        user = __create_new_user_and_add_to_db(app, db, user_manager, name, mail, pw, display_name, remote_app, roles)

    return user


def __password_is_valid(app, name, pw):
    if pw is None:
        app.logger.warn("User %s has no password specified." % name)
    elif len(pw) < 4:
        app.logger.warn("Password of user %s is too short. Please choose a password with 4 or more characters." % name)
    else:
        return True
    return False


def __get_user_from_db(name):
    return User.query.filter(User.username == name).first()


def __create_new_user_and_add_to_db(app, db, user_manager, name, mail, pw, display_name, remote_app, roles):
    user = User(active=True,
                username=name,
                displayname=display_name,
                remoteapp=remote_app,
                email=mail,
                confirmed_at=datetime.datetime.utcnow(),
                password=user_manager.hash_password(pw))

    user = __append_roles_to_user_object(app, user, roles)
    __add_user_to_db(db, user)

    return user


def __append_roles_to_user_object(app, user, roles):
    user_with_roles = user

    for r in roles:
        curr_role = __get_role_from_db(r)
        if curr_role is None:
            __log_role_query_failure(app, r)
        else:
            user_with_roles.roles.append(curr_role)

    return user_with_roles


def __get_role_from_db(role):
    return Role.query.filter(Role.name == role).first()


def __log_role_query_failure(app, role):
    app.logger.info("Unable to find role: " + str(role))


def __add_user_to_db(db, user):
    db.session.add(user)
    db.session.commit()


def init_app(app, db_instance, extra_config_settings={}):
    __init_app_config_settings(app, extra_config_settings)

    # Setup Flask-Mail
    mail = Mail(app)

    babel = Babel(app)

    # Setup Flask-User to handle user account related forms
    from webrob.models.users import User
    db_adapter = SQLAlchemyAdapter(db_instance, User)
    app.user_manager = UserManager(db_adapter, app)  # Init Flask-User and bind to app

    # Load all models.py files to register db.Models with SQLAlchemy
    from webrob.models import users
    from webrob.models import tutorials
    from webrob.models import teaching
    from webrob.models import experiments

    # Load all views.py files to register @app.routes() with Flask
    from webrob.pages import api
    from webrob.pages import db
    from webrob.pages import editor
    from webrob.pages import experiments
    from webrob.pages import knowrob
    from webrob.pages import login
    from webrob.pages import meshes
    from webrob.pages import mongo
    from webrob.pages import tutorials
    # from webrob.pages import oauth

    init_db(app, db_instance)
    init_webapp(app, db_instance)

    add_user(app=app, db=db_instance, user_manager=app.user_manager,
             name='admin',
             mail=os.environ.get('OPENEASE_MAIL_USERNAME', 'admin@openease.org'),
             pw=os.environ.get('OPENEASE_ADMIN_PASSWORD'),
             roles=['admin'])

    __log_webapp_started(app)
    return app


def __init_app_config_settings(app, extra_config_settings):
    app.config.from_object('webrob.config.settings')  # Read config from 'app/settings.py' file
    app.config.update(extra_config_settings)  # Overwrite with 'extra_config_settings' parameter
    if app.testing:
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF checks while testing
    if evg.get_variable_with_default('EASE_DEBUG', 'false') == 'true':
        app.config['DEBUG'] = True
        app.config['SECRET_KEY'] = app.config['DEV_SECRET_KEY']
    else:
        try:
            app.config['SECRET_KEY'] = open('/etc/ease_secret/secret', 'rb').read()
        except IOError:
            app.config['SECRET_KEY'] = random_string(64)


def __log_webapp_started(app):
    app.logger.info("Webapp started.")
