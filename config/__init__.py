# -*- coding: utf-8 -*- 

import json
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(PROJECT_DIR + '/local.json') as data_file:
    local = json.load(data_file)
    POSTGRES = local['postgres']
    FACEBOOK = local['facebook']
    GOOGLE = local['google']
    GITHUB = local['github']
    ENV = local.get('env', 'development')
    SPHINX = local.get('sphinx')
    REDIS = local.get('redis')

with open(PROJECT_DIR + '/../public/js/build.json') as data_file:
    build = json.load(data_file)
    REQUIREJS_CONFIG = build

LANGUAGES = {
    'vi': u'Việt Nam'
}

BABEL_DEFAULT_LOCALE = 'vi'

# The prefix path for all static files
STATIC_PATH = '/static'

# Use this version to force browsers to reload new files
STATIC_VERSION = 1

VERSION = '0.1.0'

# used for session and several other stuff
SECRET = 'ZzS6EguCw8JmrVzEsBvxz9Cs'
