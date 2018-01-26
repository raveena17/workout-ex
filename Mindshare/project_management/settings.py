# Django settings for project_management project.
import os

DEBUG = True
# TEMPLATE_DEBUG = DEBUG
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
# mindshare_jun_20_new,
DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mind_share',
        'USER': 'root',                      
        'PASSWORD': 'root',                  
        'HOST': '',
        'PORT': '',

        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'mindshare_db',
        # 'USER': 'root',                      
        # 'PASSWORD': 'root',                  
        # 'HOST': '192.168.1.76',
        # 'PORT': '3306',

    }
}

ALLOWED_HOSTS = ['*']

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
# MEDIA_URL = '/static/'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static_media/')
#STATIC_ROOT = os.path.join(PROJECT_ROOT, "media")
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static/'),)


# URL prefix for admin media -- CSS, JavaScript and images
# ADMIN_MEDIA_PREFIX = '/media/'
ADMIN_MEDIA_PREFIX = '/static/'

LOGIN_URL = '/login/'
USER_REDIRECT_URL = '/timesheet/'  # 'http://192.168.1.77/trac'#'/timesheet/'
# ADMIN_REDIRECT_URL  = '/user/list/'
ADMIN_REDIRECT_URL = '/timesheet/'

PAY_IT_STATUS_PATH = os.path.join(MEDIA_ROOT, 'PayITStatus_xl/PayITStatus.xls')

# using  mem catche
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/?timeout=0'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*mf08ik29!*+ed^f7u&px03$*is7+jz@v_o6%y63iu@%u(!9^t'

# List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# #     'django.template.loaders.eggs.Loader',
# )

# TEMPLATE_CONTEXT_PROCESSORS = (
#     "django.core.context_processors.auth",
#     "django.core.context_processors.i18n",
#     "django.core.context_processors.debug",
#     "django.core.context_processors.request",
#     "django.core.context_processors.media",
#     "django.contrib.messages.context_processors.messages",
# )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # must be after session middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.contrib.auth.forms.AuthenticationForm',

)

ROOT_URLCONF = 'project_management.urls'

# TEMPLATE_DIRS = (
#             os.path.join(PROJECT_ROOT, "templates"),
#             )


AUTHENTICATION_BACKENDS = (
    'project_management.access_control.authentication.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
    'project_management.access_control.permission.ObjectPermission',

)

# AUTH_PROFILE_MODULE = 'users.UserProfile'
AUTH_PROFILE_MODULE = 'user_profile.UserProfile'

LDAP_SERVER = '192.168.1.3'
# Local host = '192.168.1.102:9073'
""" Project e-mail related """
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/app-messages'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'raveena@5gindia.net'
EMAIL_HOST_PASSWORD = '17041996'
# EMAIL_HOST_USER = 'itadmin@5gindia.net'
# EMAIL_HOST_PASSWORD = 'Fiveg2011'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_MESSAGE_GREE = 'Hello, '
EMAIL_MESSAGE_TXT = 'You have been successfully registered in payit. '
EMAIL_MESSAGE_TXT1 = 'login in to the following url to '
EMAIL_MESSAGE_TXT2 = ''
EMAIL_MESSAGE = EMAIL_MESSAGE_GREE + "\n\t" + EMAIL_MESSAGE_TXT + "\n" + EMAIL_MESSAGE_TXT1 + "\n" +\
    EMAIL_MESSAGE_TXT2 + "\n\t Username = %s \n\t Password = %s "
EMAIL_CONTENT_TYPE = 'html'
MAIL_LOG_FILE = os.path.join(PROJECT_ROOT, 'mail_errorlog.txt')

USER_CREATION_EMAIL_SUBJECT = 'payit registration'
USER_CREATION_EMAIL_MESSAGE = EMAIL_MESSAGE_GREE + "\n\t" + EMAIL_MESSAGE_TXT

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
LOG_TEMPLATE = ''  # '/home/username/projects/payit/payit/dataTemplate'
LOG_POST_PATH = ''  # '/home/username/projects/payit/payit'
EVENT_PATH = ''  # '/home/username/projects/payit/payit'

""" setting update configuration """
SETTING_PATH = ''  # '/home/username/projects/payit/payit/apps'
#TEST_RUNNER = 'coverage.test_coverage.coverage_runner.run_tests'

""" PIE Chart Colors """
ON_SCHEDULE = '#8887ff'
AHEAD_SCHEDULE = '#33ff33'
BEHIND_SCHEDULE = '#ff3333'

"""Project Reminder"""
ALERT_ON = 2
ALERT_REMINDER = 2

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #'coverage',
    'pagination',
    'mptt',
    'django_cron',
    'newsletter',
    'announcements',
    'django_tables2',
    'bootstrap3',
    'bootstrapform',
    
    #'memcache_status',
    # 'client_visit_report',
    # 'customer',
    # 'cvr',
    # 'projects',
    # 'client_visit_report.apps.client_visit_reportAppConfig',
    'project_management.projectbudget',
    'project_management.fields',
    'project_management.logs',
    'project_management.access_control',
    'project_management.address',
    'project_management.alert',
    'project_management.business_unit',
    'project_management.users',
    'project_management.conferenceroombooking',
    'project_management.projects',
    'customer',

    'project_management.client_visit_report',

    'project_management.notifications',
    'project_management.repository',
    'project_management.non_project_task',
    'project_management.tasks',
    'project_management.common_manager',
    'project_management.timesheet',
    'project_management.timesheetnew',
    'project_management.milestone',
    'project_management',
    'project_management.management',
    'project_management.reimbursement',
    'project_management.travel',

    #'project_management.performance_measurement',

    'project_management.code_review'
    #'project_management.codereview_matrix',
    # 'rest_framework',

)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, "templates"),
        ],
        'OPTIONS':{
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                # 'django.core.context_processors.request',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    }
]


# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 # Already defined Django-related contexts here

#                 # `allauth` needs this from django
#                 'django.template.context_processors.request',
#             ],
#         },
#     },
# ]

# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# #     'django.template.loaders.eggs.Loader',
# )


try:
    from local_settings import *
except ImportError:
    pass
