from flask import request, render_template, jsonify, abort

import json

from webrob.app_and_db import app
from webrob.utility.utility import admin_required
from webrob.models.db import *

__author__ = 'danielb@cs.uni-bremen.de'


@app.route('/db/docu/<key>', methods=['POST'])
def db_docu_text(key):
    docs = _get_all_docs()
    for d in docs:  # find specific
        if d.key == key:
            return jsonify(result=d.text)
    _display_warning_when_unable_to_find_docu(key)


def _get_all_docs():
    db_adapter = current_app.user_manager.db_adapter
    return db_adapter.find_all_objects(db_table_class('docu'))


def _display_warning_when_unable_to_find_docu(key):
    app.logger.warn("Unable to find docu for: " + str(key) + ".")
    abort(404)


@app.route('/db/page/user_roles')
@admin_required
def db_page_user_roles():
    return render_template('admin/db_user_roles.html', **locals())


@app.route('/db/find/user_roles', methods=['POST'])
@admin_required
def db_find_user_roles():
    users = _get_all_users()
    user_roles = []
    for u in users:     # find user roles
        user_roles.append({
            'id': u.id,
            'name': u.username,
            'roles': map(lambda r: {'name': r.name}, u.roles)
        })
    return jsonify(result=user_roles)


def _get_all_users():
    db_adapter = current_app.user_manager.db_adapter
    return db_adapter.find_all_objects(db_table_class('user'))


@app.route('/db/save/user_roles', methods=['POST'])
@admin_required
def db_save_user_roles():
    data = json.loads(request.data)
    if 'roles' in data and 'id' in data:
        _save_roles_to_users_and_commit_to_db(data)
    else:
        app.logger.warn("Invalid input data.")
    return jsonify(result=None)


def _save_roles_to_users_and_commit_to_db(data):
    db_adapter = current_app.user_manager.db_adapter
    user = db_find(db_table_class('user'), data['id'])
    for r in data['roles']:
        role = db_find_name(db_table_class('role'), r['name'])
        if role is not None:
            user.roles.append(role)
    db_adapter.commit()


@app.route('/db/page/<table>')
@admin_required
def db_page_route(table):
    table_class = db_table_class(table)
    if table_class is None:
        app.logger.warn("Unable to find table for: " + str(table) + ".")
        abort(404)

    columns = db_columns(table_class)
    for c in columns:
        if str(c['type']) == 'BOOLEAN':
            c['type'] = 'boolean'
        elif str(c['type']) == 'DATETIME':
            c['type'] = 'date'
        elif str(c['type']) == 'INTEGER':
            c['type'] = 'number'
            c['format'] = '{0:d}'
        # elif str(c['type']) == 'BLOB':
        else:
            c['type'] = 'string'

        c['editable'] = c['name'] is not 'id'
        if c['editable']:
            c['editable'] = 'true'
        else:
            c['editable'] = 'false'

        if c['nullable']:
            c['nullable'] = 'true'
        else:
            c['nullable'] = 'false'

    return render_template('admin/db_table.html', **locals())


@app.route('/db/find/<table>', methods=['POST'])
@admin_required
def db_find_route(table):
    return jsonify(result=db_find_all(db_table_class(table)))


@app.route('/db/save/<table>', methods=['POST'])
@admin_required
def db_update_route(table):
    data = json.loads(request.data)
    cls = db_table_class(table)
    if data is not None:
        if 'id' in data and db_find(cls, data['id']):
            db_update(cls, data['id'], data)
        else:
            db_create(cls, data)
    return jsonify(result=None)


@app.route('/db/new/<table>', methods=['POST'])
@admin_required
def db_create_route(table):
    data = json.loads(request.data)
    if data is not None:
        db_create(db_table_class(table), data)
    return jsonify(result=None)


@app.route('/db/delete/<table>', methods=['POST'])
@admin_required
def db_remove_route(table):
    data = json.loads(request.data)
    cls = db_table_class(table)
    if data is not None and 'id' in data and db_find(cls, data['id']):
        db_remove(cls, data['id'])
    return jsonify(result=None)
