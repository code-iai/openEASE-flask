import webrob.utility.environment_variable_getter as evg

# TODO: Shouldn't this be generated randomly???
DEV_SECRET_KEY = '\\\xf8\x12\xdc\xf5\xb2W\xd4Lh\xf5\x1a\xbf"\x05@Bg\xdf\xeb>E\xd8<'

# TODO: Adjust URI to project-settings, check docker-compose from openease-knowrob
# Potentially use environment variables
# dialect+driver://username:password@host:port/database
# SQLALCHEMY_DATABASE_URI = 'postgresql://docker@postgres_db:5432/docker'
# SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'postgresql://docker@localhost:5432/docker'  # currently only for testing

CSRF_ENABLED = True

# email server
MAIL_SERVER = evg.get_variable_with_default('OPENEASE_MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(evg.get_variable_with_default('OPENEASE_MAIL_PORT', '465'))
MAIL_USE_TLS = bool(evg.get_variable_with_default('OPENEASE_MAIL_USE_TLS', 'False'))
MAIL_USE_SSL = bool(evg.get_variable_with_default('OPENEASE_MAIL_USE_SSL', 'True'))
MAIL_USERNAME = evg.get_variable_with_default_none('OPENEASE_MAIL_USERNAME')
# possibly remove default returns, https://github.com/code-iai/openEASE-flask/issues/4
MAIL_PASSWORD = evg.get_variable_with_default('OPENEASE_MAIL_PASSWORD', '12345678')
MAIL_DEFAULT_SENDER = '"Sender" <openease.iai@gmail.com>'

FACEBOOK_APP_TOKENS = (evg.get_variable_with_default_none('FACEBOOK_APP_ID'),
                       evg.get_variable_with_default_none('FACEBOOK_APP_SECRET'))
TWITTER_APP_TOKENS = (evg.get_variable_with_default_none('TWITTER_APP_ID'),
                      evg.get_variable_with_default_none('TWITTER_APP_SECRET'))
GITHUB_APP_TOKENS = (evg.get_variable_with_default_none('GITHUB_APP_ID'),
                     evg.get_variable_with_default_none('GITHUB_APP_SECRET'))
GOOGLE_APP_TOKENS = (evg.get_variable_with_default_none('GOOGLE_APP_ID'),
                     evg.get_variable_with_default_none('GOOGLE_APP_SECRET'))

USER_ENABLE_USERNAME = True
USER_ENABLE_EMAIL = True
USER_ENABLE_CONFIRM_EMAIL = False

MAX_HISTORY_LINES = 100

MESH_REPOSITORIES = map(lambda x: tuple(x.split(' ')),
                        evg.get_variable_with_default('OPENEASE_MESHES', 'git https://github.com/PR2/pr2_common').split(
                            ','))

ROS_DISTRIBUTION = evg.get_variable_with_default_none('OPENEASE_ROS_DISTRIBUTION')
