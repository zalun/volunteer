# settings for the jsFiddle
import os
import django.conf.global_settings as DEFAULT_SETTINGS

ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Change it to False on development machines
PRODUCTION = True

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': path('development.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        #'OPTIONS': {'init_command': 'SET storage_engine=InnoDB; SET foreign_key_checks = 0'},
        #'TEST_CHARSET': 'utf8',
        #'TEST_COLLATION': 'utf8_general_ci',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Registration
LOGIN_URL = '/account/signin/'
REGISTER_URL = '/account/signup'
LOGIN_REDIRECT_URL = '/'     # '/user/dashboard/'
REGISTER_REDIRECT_URL = '/'  # '/user/dashboard/'
AUTH_PROFILE_MODULE = 'person.Profile'

# System will look for media in these directories and use MEDIA_ROOT
# if failed
# This shouldn't be used in production. Configure WebServer to serve these
# directly from the filesystem
MEDIA_ROOTS = ()

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# This shouldn't be used in production. Configure WebServer to serve these
# directly from the filesystem
MEDIA_ROOT = path('media')
UPLOADS_ROOT = path('media/uploads')

# Place media needed to be used from apps in their media directories
APP_MEDIA_PREFIX = path('apps')
APP_MEDIA_SUFFIX = 'media'

# Where to upload the frameworks (absolute path)
#FRAMEWORKS_DIR = path('frameworks')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

STATIC_ROOT = path('static')
STATIC_URL = '/static/'
STATICFILES_FINDERS = DEFAULT_SETTINGS.STATICFILES_FINDERS + (
    'compressor.finders.CompressorFinder',
)


# Nose tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s '
                      '%(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s (%(name)s.%(funcName)s) %(message)s'
        },
        'syslog': {
            'format': '%(asctime)s %(levelname)s: '
                      '(%(name)s.%(funcName)s#%(lineno)d) %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'syslog'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'cms': {
            'propagate': True,
            'handlers': ['console', 'syslog'],  # , 'mail_admins'],
            'level': 'INFO',
        }
    }
}


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# This shouldn't be used in production. Configure WebServer to serve these
# directly from the filesystem
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'Secret Key'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'fiber.context_processors.page_info',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # django-fiber
    'fiber.middleware.ObfuscateEmailAddressMiddleware',
    'fiber.middleware.AdminPageMiddleware',
    'fiber.middleware.PageFallbackMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    path('templates'),
    # Put strings here, like "/home/html/django_templates"
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    #server
    'gunicorn',
    # DEV
    'django_nose',
    # CMS APPS
    'base',
    'piston',
    'mptt',
    'compressor',
    'fiber',
    # Admin
    'django.contrib.admin',
    'django.contrib.admindocs',
]

DEV_APPS = (
    'django_nose',
)
# Which from above Middleware classes should be removed if in PRODUCTION


# Fiddle settings
FIDDLE_HASHTAG_LENGTH = 5
