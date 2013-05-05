import os, manage, django

from django.core.exceptions import ImproperlyConfigured

msg = 'Set the %s environment variable'

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except:
        error_msg = msg % var_name
        raise ImproperlyConfigured(error_msg)
    

MAILCHIMP_API = os.environ['MAILCHIMP_API']
MAILCHIMP_LIST_ZV = os.environ['MAILCHIMP_LIST_ZV']

# email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT =  587
EMAIL_HOST_USER = 'zaalvoetbalhercules@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

# directory settings
SITE_ROOT = os.path.dirname(os.path.realpath(manage.__file__))
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
BUCKET = 'elasticbeanstalk-eu-west-1-244582788776'

ADMINS = (
    ('Ben Teeuwen', 'bteeuwen@gmail.com'),
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {}

# amazon database settings
# try:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#             'NAME': os.environ['RDS_DB_NAME'],
#             'USER': os.environ['RDS_USERNAME'],
#             'PASSWORD': os.environ['RDS_PASSWORD'],
#             'HOST': os.environ['RDS_HOSTNAME'],
#             'PORT': os.environ['RDS_PORT'],
#         }
#     }
# except:
#     pass

DEBUG = TEMPLATE_DEBUG = False

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'nl-NL'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
#MEDIA_URL = ''
MEDIA_URL = 'https://' + BUCKET + 's3.amazonaws.com/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = 'https://' + BUCKET + 's3.amazonaws.com/static/'
#STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')

# STATIC_ROOT = os.path.join(
#  os.path.dirname(
#   os.path.dirname(
#    os.path.abspath(__file__))),'static')

DEFAULT_FILE_STORAGE ='storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE ='storages.backends.s3boto.S3BotoStorage'
# DEFAULT_FILE_STORAGE = 'mijnhercules.s3utils.MediaRootS3BotoStorage'
# STATICFILES_STORAGE = 'mijnhercules.s3utils.StaticRootS3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = BUCKET
AWS_PRELOAD_METADATA = True # necessary to fix manage.py collectstatic command to only upload changed files instead of all files

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
#STATIC_URL = '/static/'
STATIC_URL = 'https://' + BUCKET + '.s3.amazonaws.com/'
ADMIN_MEDIA_PREFIX = 'https://' + BUCKET + 's3.amazonaws.com/admin'


# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'staticfiles'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['SECRET_KEY']

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'mijnhercules.middleware.LastSiteUrl',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mijnhercules.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mijnhercules.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates')
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    
    # self-written apps
    'members', # player data
    'matches', # soccer matches (substitutes, viewing, importing)
    'newsletters', # mailchimp integration
    # 3rd party apps
    'djcelery',
    'south',
    # 'guardian',
    'storages',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


## object permissions plugin Guardian specific settings:
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    # 'guardian.backends.ObjectPermissionBackend',
)

## to map User on Player:
AUTH_PROFILE_MODULE='members.Player'
# AUTH_USER_MODEL = 'auth.User'
# ANONYMOUS_USER_ID = -1
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'

# enable global accessible data (e.g. player name, team name, program, substitutes info)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'mijnhercules.context_processors.playerContext',
    'mijnhercules.context_processors.substitutesNeeded',
    # 'mijnhercules.context_processors.substitutesAvailable',
)

#south migration files, e.g. guardian, inside version control.
SOUTH_MIGRATION_MODULES = {
    # 'guardian': 'mijnhercules.migrations.guardian',
}

# celery task management settings
import djcelery
djcelery.setup_loader()

# The backend used to store task results - because we're going to be 
# using RabbitMQ as a broker, this sends results back as AMQP messages
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("members.tasks", )
CELERY_ALWAYS_EAGER = True

from celery.schedules import crontab
# The default Django db scheduler
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERYBEAT_SCHEDULE = {}