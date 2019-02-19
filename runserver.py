# This file starts the WSGI web application.
# - Heroku starts gunicorn, which loads Procfile, which starts runserver.py
# - Developers can run it from the command line: python runserver.py

from webrob.app_and_db import app, db
from webrob.startup.init_app import init_app
from webrob.pages.meshes import update_meshes
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


def __config_is_debug():
    return 'DEBUG' in app.config and app.config['DEBUG']


def __run_debug_server():
    print 'Run web server in DEBUG mode'
    app.run(host='0.0.0.0')


def __run_server():
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    print 'Web server is running. Listening on {}'.format(5000)
    IOLoop.instance().start()


init_app(app, db)

# Start a development web server if executed from the command line
if __name__ == '__main__':
    # TODO: meshes-module needs to be refactored
    update_meshes()
    if __config_is_debug():
        __run_debug_server()
    else:
        __run_server()
