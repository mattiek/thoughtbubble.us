"""
Django settings for thoughtbubble project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
BASE_ROOT = os.path.join(SITE_ROOT, '../..')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q7u5$ma-1t0(le9l@ku=ki8x%%dd860ub5s$6bfwyep@cc8scy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'thoughtbubble',
    'world',
    # 'neighborhood',
    'cities',
    'location',
    'idea',
    'csvimport',
    'gunicorn',
    'south',
    'widget_tweaks',
    'rest_framework',
    'api',
    'floppyforms',
    'supportering',
    'commenteering',
    'organization',
    'project',
    'partner',
    'tbnews',
    # 'social.apps.django_app.default',
    'threadedcomments',
    'avatar',
    'django.contrib.comments',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.twitter',
    'django_extensions',
)

COMMENTS_APP = 'threadedcomments'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

ROOT_URLCONF = 'thoughtbubble.urls'

WSGI_APPLICATION = 'thoughtbubble.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'thoughtbubble',                      # Or path to database file if using sqlite3.
        'USER': 'brandon',                      # Not used with sqlite3.
        'PASSWORD': 'colonel1',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

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


MEDIA_ROOT = os.path.join(os.path.join(BASE_ROOT, '..'), 'thoughtbubble-media/media')
STATIC_ROOT = os.path.join(os.path.join(BASE_ROOT, '..'), 'thoughtbubble-static/static')

AUTH_USER_MODEL = 'thoughtbubble.ThoughtbubbleUser'

MAPQUEST_KEY = 'Fmjtd%7Cluub250ylu%2Ca2%3Do5-9uzl16'

REST_FRAMEWORK = {
    'PAGINATE_BY': 10
}

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'thoughtbubble.processors.login_form',
    'thoughtbubble.processors.domain_host',
    'thoughtbubble.processors.exploring',
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    # 'social.apps.django_app.context_processors.backends',
    # 'social.apps.django_app.context_processors.login_redirect',
]

AUTHENTICATION_BACKENDS = (
# Needed to login by username in Django admin, regardless of `allauth`
"django.contrib.auth.backends.ModelBackend",

# `allauth` specific authentication methods, such as login by e-mail
"allauth.account.auth_backends.AuthenticationBackend",
)

# AUTHENTICATION_BACKENDS = (
#     'social.backends.twitter.TwitterOAuth',
#     'social.backends.linkedin.LinkedinOAuth2',
#     'social.backends.facebook.FacebookOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
# )

SITE_ID = 1

SOUTH_TESTS_MIGRATE = False

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

SOCIALACCOUNT_AUTO_SIGNUP=False
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_EMAIL_VERIFICATION="none"
SOCIALACCOUNT_ADAPTER="thoughtbubble.views.MySocialAdapter"