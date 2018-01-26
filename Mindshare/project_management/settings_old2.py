# Django settings for project_management project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mindshare',                      # Or path to database file if using sqlite3.
        'USER': 'mindshare',                      # Not used with sqlite3.
        'PASSWORD': 'Fiveg',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'Asia/Calcutta'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
#LANGUAGE_CODE = 'ta'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

import os.path
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images
ADMIN_MEDIA_PREFIX = '/media/'

LOGIN_URL = '/login/'
USER_REDIRECT_URL  = '/timesheet/'#'http://192.168.1.77/trac'#'/timesheet/'
ADMIN_REDIRECT_URL  = '/user/list/'

#using  mem catche
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/?timeout=0'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*mf08ik29!*+ed^f7u&px03$*is7+jz@v_o6%y63iu@%u(!9^t'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware', #must be after session middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'project_management.urls'

TEMPLATE_DIRS = (
            os.path.join(PROJECT_ROOT, "templates"),
            )

AUTHENTICATION_BACKENDS = (
    'project_management.access_control.authentication.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
    'project_management.access_control.permission.ObjectPermission',
)

AUTH_PROFILE_MODULE = 'users.UserProfile'

LDAP_SERVER = '192.168.1.4'


""" Project e-mail related """
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ' itadmin@5gindia.net'
EMAIL_HOST_PASSWORD = 'Fiveg2011'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_MESSAGE_GREE = 'Hello, '
EMAIL_MESSAGE_TXT = 'You have been successfully registered in payit. '
EMAIL_MESSAGE_TXT1 = 'login in to the following url to '
EMAIL_MESSAGE_TXT2 = ''
EMAIL_MESSAGE = EMAIL_MESSAGE_GREE + "\n\t" + EMAIL_MESSAGE_TXT + "\n" + EMAIL_MESSAGE_TXT1 + "\n" +\
                EMAIL_MESSAGE_TXT2 + "\n\t Username = %s \n\t Password = %s "

USER_CREATION_EMAIL_SUBJECT = 'payit registration'
USER_CREATION_EMAIL_MESSAGE = EMAIL_MESSAGE_GREE+"\n\t"+ EMAIL_MESSAGE_TXT

NONPROJECT_TASK_ASSIGN_UNASSIGN = 'You have been assigned/unassigned in task %s'

RESET_PWD_EMAIL_MESSAGE = "Welcome,\n\t Your password have been reset successfully.\n\t Username = %s \n\t Password = %s "

FEEDBACK_MESSAGE = "Hello,\n\t You have received a feedback from : %s with E-mail : %s.\n\n\t Rating = %s \n\n\t Comment = %s \n\n\t Suggestion = %s "
##EMAIL_HOST = 'mail.fifthgentech.com'
""" MAX_FILE_SIZE values is in bytes """
MAX_FILE_SIZE = 10000000
FILE_EXTENSIONS_TO_EXCLUDE = ['.exe', '.py', '.sh', '.bat', '.mis', '.dll']
LOGO_PATH = '/css/images'

""" List page setting """
IS_PAGINATION = True
PAGE_SIZE = 10
LOGIN_ATTEMPTS = 5
DASHBOARD_PAGE_SIZE = 5

DATE_FORMAT = 'm-d-Y'
TEMPLATE_COLOR = 'blue'
LIST_DATE_FORMAT = '%b %d, %Y'
TIMESPAN_DATE_FORMAT = '%b %d'

""" Logs to log in the Portal Apps"""
LOG_TEMPLATE = '' #'/home/username/projects/payit/payit/dataTemplate'
LOG_POST_PATH = '' #'/home/username/projects/payit/payit'
EVENT_PATH = '' #'/home/username/projects/payit/payit'

""" setting update configuration """
SETTING_PATH = '' #'/home/username/projects/payit/payit/apps'
#TEST_RUNNER = 'coverage.test_coverage.coverage_runner.run_tests'

""" PIE Chart Colors """
ON_SCHEDULE = '#8887ff'
AHEAD_SCHEDULE = '#33ff33'
BEHIND_SCHEDULE = '#ff3333'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    #'coverage',
    'pagination',
    'mptt',
    'django_cron',
    'announcements',
    'endless_pagination',
    #'memcache_status',
    'project_management.fields',
    'project_management.logs',
    'project_management.access_control',
    'project_management.address',
    'project_management.business_unit',
    'project_management.users',
    'project_management.projects',
    'project_management.notifications',
    'project_management.repository',
    'project_management.non_project_task',
    'project_management.tasks',
    'project_management.common_manager',
    'project_management.timesheet',
    'project_management.customer',
    'project_management.milestone',
    'project_management',
)

try:
    from local_settings import *
except ImportError:
    pass
