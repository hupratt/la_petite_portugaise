# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...) f
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

SECRET_KEY = os.environ.get("SECRET_KEY_lpp")


ALLOWED_HOSTS = ["www.lapetiteportugaise.eu", "localhost", "127.0.0.1", "lapetiteportugaise.eu"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "posts",
    "klingon",
    "robots",
    "pagedown",
    'corsheaders'
]

INTERNAL_IPS = ['127.0.0.1']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOW_HEADERS = ['*']

# sitemap parameter

SITE_ID = 3

MIDDLEWARE = [
    "la_petite_portugaise.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]


ROOT_URLCONF = "la_petite_portugaise.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "la_petite_portugaise", "templates"),
            os.path.join(BASE_DIR, "la_petite_portugaise", "templates", "error"),
            os.path.join(BASE_DIR, "la_petite_portugaise", "templates", "index"),
            os.path.join(BASE_DIR, "la_petite_portugaise", "templates", "events"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "la_petite_portugaise.context_processors.ga_tracking_id",
                "la_petite_portugaise.context_processors.this_year",
                "la_petite_portugaise.context_processors.facebook_retrieve",
                "la_petite_portugaise.context_processors.is_mobile",
            ],
            "libraries": {"formatter": "la_petite_portugaise.templatetags.formatter",},
        },
    },
]

WSGI_APPLICATION = "la_petite_portugaise.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if os.environ.get("DJANGO_DEVELOPMENT") is not None:
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("enginedb"),
            "NAME": "lapetiteportugaise",
            "USER": os.environ.get("dbuser"),
            "PASSWORD": os.environ.get("dbpassword"),
            "HOST": os.environ.get("hostip"),  # hostipdev
            "PORT": os.environ.get("pnumber"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "lapetiteportugaise",
            "USER": os.environ.get("dbuser"),
            "PASSWORD": os.environ.get("dbpassword"),
            "HOST": os.environ.get("hostip"),
            "PORT": os.environ.get("pnumber"),
        }
    }

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Luxembourg"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")  # store files
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


KLINGON_DEFAULT_LANGUAGE = "en"


def ugettext(s):
    return s


LANGUAGES = (
    ("en", _("English")),
    ("de", _("German")),
    ("fr", _("French")),
    ("pt", _("Portuguese")),
)


LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)


DJANGO_ADMIN_URL = "admin/"


GA_TRACKING_ID = os.environ.get("GA_TRACKING_ID")
GOOGLE_RECAPTCHA_SECRET_KEY = os.environ.get("GOOGLE_RECAPTCHA_SECRET_KEY")
GOOGLE_RECAPTCHA_SITE_KEY = os.environ.get("GOOGLE_RECAPTCHA_SITE_KEY")


# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
EMAIL_HOST_RECIPIENT = "lapetiteportugaise.bxl@gmail.com"
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

if os.environ.get("DJANGO_DEVELOPMENT") is not None:
    DEBUG = True
    EMAIL_HOST_RECIPIENT = "cortohprattdo@gmail.com"



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(name)s.%(funcName)s:%(lineno)s- %(message)s"
        },
        "simple": {"format": "{levelname} {message}", "style": "{"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "error.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            # output logs to the console and to the file
            "level": "INFO",
            "handlers": ["file", "console"],
            "propagate": True,
        }
    },
}

if os.environ.get("DJANGO_DEVELOPMENT") is None:
    # Sentry
    import sentry_sdk  # pylint: disable=import-error
    from sentry_sdk.integrations.django import (
        DjangoIntegration,
    )  # pylint: disable=import-error
    SENTRY_KEY = os.environ.get("SENTRY_KEY")

    sentry_sdk.init(
        dsn="https://"
        + SENTRY_KEY
        + "@sentry.io/1467229",  
        integrations=[DjangoIntegration()],
    )
    # SECURITY

    SECURE_HSTS_SECONDS = 31536000
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True

# django-robots

ROBOTS_SITEMAP_URLS = [
    "https://www.lapetiteportugaise.eu/sitemap.xml",
]

ROBOTS_SITEMAP_VIEW_NAME = "sitemap"


# CORS_ORIGIN_WHITELIST = (
#     "http://localhost:8000",
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
#     "http://127.0.0.1:8000",
#     "https://shop.lapetiteportugaise.eu",
#     "https://connect.facebook.net",
#     "https://connect.facebook.net/nl_BE/sdk.js#xfbml=1&version=v11.0."
# )

# CORS_ALLOWED_ORIGIN_REGEXES = [
# r"^(https:\/\/\w+.facebook.net\/[\s\S]*)",
# ]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = False