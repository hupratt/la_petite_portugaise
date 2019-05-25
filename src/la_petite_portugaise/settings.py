# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...) f
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/ 

if os.environ.get('DJANGO_DEVELOPMENT') is not None:
    SECRET_KEY = os.environ.get('SECRET_KEY_lpp')


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'posts',
    'klingon',
    'robots',
]

# sitemap parameter

SITE_ID = 3

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'la_petite_portugaise.middleware.MobileDetectionMiddleware',
]


ROOT_URLCONF = 'la_petite_portugaise.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'la_petite_portugaise', 'templates'),
                 os.path.join(BASE_DIR, 'la_petite_portugaise', 'templates', 'error'),
                 os.path.join(BASE_DIR, 'la_petite_portugaise', 'templates', 'index'),
                 os.path.join(BASE_DIR, 'la_petite_portugaise', 'templates', 'events')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'la_petite_portugaise.context_processors.ga_tracking_id',
                'la_petite_portugaise.context_processors.this_year',
                'la_petite_portugaise.context_processors.facebook_retrieve',
                'la_petite_portugaise.context_processors.is_mobile',
            ],
        },
    },
]

WSGI_APPLICATION = 'la_petite_portugaise.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if os.environ.get('DJANGO_DEVELOPMENT') is not None:
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('enginedb'),
            'NAME': os.environ.get('dbname'),
            'USER': os.environ.get('dbuser'),
            'PASSWORD': os.environ.get('dbpassword'),
            'HOST': os.environ.get('hostipdev'), #hostipdev
            'PORT': os.environ.get('pnumber'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'lapetiteportugaise',
            'USER': os.environ.get('dbuser'),
            'PASSWORD': os.environ.get('dbpassword'),
            'HOST': os.environ.get('hostip'),
            'PORT': os.environ.get('pnumber'),
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Luxembourg'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")  # store files
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


KLINGON_DEFAULT_LANGUAGE = 'en'


def ugettext(s): return s


LANGUAGES = (
    ('en', _('English')),
    ('de', _('German')),
    ('fr', _('French')),
    ('pt', _('Portuguese')),
)


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


DJANGO_ADMIN_URL = 'admin/'


GA_TRACKING_ID = os.environ.get('GA_TRACKING_ID')
GOOGLE_RECAPTCHA_SECRET_KEY = os.environ.get('GOOGLE_RECAPTCHA_SECRET_KEY')
GOOGLE_RECAPTCHA_SITE_KEY = os.environ.get('GOOGLE_RECAPTCHA_SITE_KEY')


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_RECIPIENT = 'lapetiteportugaise.bxl@gmail.com'

if os.environ.get('DJANGO_DEVELOPMENT') is not None:
    DEBUG = True
    EMAIL_HOST_RECIPIENT = 'cortohprattdo@gmail.com'


# Sentry

if os.environ.get('DJANGO_DEVELOPMENT') is None:
    import sentry_sdk # pylint: disable=import-error
    from sentry_sdk.integrations.django import DjangoIntegration # pylint: disable=import-error

    sentry_sdk.init(
        dsn="https://"+SENTRY_KEY+"@sentry.io/1467229", # pylint: disable=undefined-variable
        integrations=[DjangoIntegration()]
    )

# django-robots 

ROBOTS_SITEMAP_URLS = [
    'https://www.lapetiteportugaise.eu/sitemap.xml',
]

ROBOTS_SITEMAP_VIEW_NAME = 'sitemap'