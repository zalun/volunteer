import os

# jsFiddle generic pplications
APPS = ['base', 'office', 'person', 'serve']
ALLAPPS = APPS[:]

PROJECT_DEV = 0         # edit all apps
PROJECT_PRODUCTION = 1  # do not edit

GIT_ORIGIN = None

# install APPS from master branch, but do not prepare them to be edited
PROJECT_TYPE = PROJECT_PRODUCTION

SERVERS = {
        'local': 'localhost',
        'stage': None,
        'production': None}

BRANCH = {
        'local': 'master',
        'production': 'production'}

# Directory project files
# Uses the fabfile as reference
LOCAL_DIR = {
        'local': os.path.abspath(os.path.dirname(__file__)),
        'production': None}

# usually directory above LOCAL_DIR - used to install apps for EDGE
MAIN_DIR = {
        'local': '/'.join(LOCAL_DIR['local'].split('/')[0:-1]),
        'production': None}

# Projectname defaults to lowercase main directory name
PROJECT_NAME = MAIN_DIR['local'].split('/')[-1].lower()

# Virtual environment name default to current PROJECT_NAME
VIRTUALENV = {
        'local': PROJECT_NAME,
        'production': PROJECT_NAME}

# Location of the virtualenvwrapper script
VE_WRAPPER = {
        'local': '/usr/local/bin/virtualenvwrapper.sh',
        'production': '/usr/local/bin/virtualenvwrapper.sh'}

WORKON_HOME = {
        'local': '~/Environments',
        'production': None}

# coverage settings
COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'settings$', '^urls$', 'locale$',
    '__init__', 'django',
    'migrations', 'fixtures', 'features',
]
# ---------------------
# This is not used yet

# defaults to projectname and $HOME defaults to /opt/DEPLOY_USER
DEPLOY_USER = PROJECT_NAME
USER_HOME = "/opt/%s" % DEPLOY_USER

# Database name and user default to project user
DATABASE_USER = DEPLOY_USER
DATABASE_NAME = PROJECT_NAME
