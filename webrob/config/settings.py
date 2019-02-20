import os
import environment_variable_getter as evg

DEV_SECRET_KEY='\\\xf8\x12\xdc\xf5\xb2W\xd4Lh\xf5\x1a\xbf"\x05@Bg\xdf\xeb>E\xd8<'

# TODO: Code in comment can possibly be removed
# = 'postgresql://docker@' + \
#     os.environ['POSTGRES_PORT_5432_TCP_ADDR'] + ':' + \
#     os.environ['POSTGRES_PORT_5432_TCP_PORT'] + '/docker'
# SQLALCHEMY_DATABASE_URI = 'postgresql://docker@' + \
#    evg.get_variable_with_default('POSTGRES_PORT_5432_TCP_ADDR', 'localhost') + ':' + \
#    evg.get_variable_with_default('POSTGRES_PORT_5432_TCP_PORT', '5432') + '/docker'

SQLALCHEMY_DATABASE_URI = 'postgresql://docker@postgres_db:5432/docker'
#SQLALCHEMY_ECHO = True

CSRF_ENABLED = True

# email server
MAIL_SERVER   = os.environ.get('OPENEASE_MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT     = int(os.environ.get('OPENEASE_MAIL_PORT', '465'))
MAIL_USE_TLS  = bool(os.environ.get('OPENEASE_MAIL_USE_TLS', 'False'))
MAIL_USE_SSL  = bool(os.environ.get('OPENEASE_MAIL_USE_SSL', 'True'))
MAIL_USERNAME = os.environ.get('OPENEASE_MAIL_USERNAME')
# TODO: Possibly remove default return. Also possibly change all environ.gets to use our module environment-variable-getter
MAIL_PASSWORD = os.environ.get('OPENEASE_MAIL_PASSWORD', '12345678')
MAIL_DEFAULT_SENDER = '"Sender" <openease.iai@gmail.com>'

FACEBOOK_APP_TOKENS = (os.environ.get('FACEBOOK_APP_ID'), os.environ.get('FACEBOOK_APP_SECRET'))
TWITTER_APP_TOKENS  = (os.environ.get('TWITTER_APP_ID'), os.environ.get('TWITTER_APP_SECRET'))
GITHUB_APP_TOKENS   = (os.environ.get('GITHUB_APP_ID'), os.environ.get('GITHUB_APP_SECRET'))
GOOGLE_APP_TOKENS   = (os.environ.get('GOOGLE_APP_ID'), os.environ.get('GOOGLE_APP_SECRET'))

USER_ENABLE_USERNAME = True
USER_ENABLE_EMAIL = True
USER_ENABLE_CONFIRM_EMAIL = False

MAX_HISTORY_LINES = 100

MESH_REPOSITORIES = map(lambda x: tuple(x.split(' ')),
                        os.getenv('OPENEASE_MESHES', 'git https://github.com/PR2/pr2_common').split(','))

# TODO: Can possibly remove this comment
# ROS_DISTRIBUTION = os.getenv('OPENEASE_ROS_DISTRIBUTION', 'indigo')

ROS_DISTRIBUTION = os.getenv('OPENEASE_ROS_DISTRIBUTION')