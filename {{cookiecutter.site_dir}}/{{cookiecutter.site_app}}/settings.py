"""
Django settings for {{ cookiecutter.site_name }}.

"""

import logging.config
import os

from django.core.exceptions import ImproperlyConfigured
{%- if cookiecutter.use_structlog == "y" %}

import structlog
{%- endif %}


def get_env_boolean(var_name, default=None):
    return os.environ.get(var_name, default).lower() not in ["false", "0"]


def get_env_list(var_name, default=None, delimiter=","):
    values = os.environ.get(var_name).split(delimiter)
    return [value.strip() for value in values]


ENV = os.environ["ENV"]

if ENV not in ("dev", "prod", "staging", "test"):
    raise ImproperlyConfigured("Unknown environment for settings: " + ENV)

DEBUG = get_env_boolean("DEBUG", False)

if ENV == "prod" and DEBUG:
    raise ImproperlyConfigured("DEBUG = True is not allowed in production")


# #########
#   PATHS
# #########

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ENV in ("prod", "staging"):
    MEDIA_ROOT = os.environ["MEDIA_ROOT"]
    STATIC_ROOT = os.environ["STATIC_ROOT"]
else:
    # No need for static root in development
    MEDIA_ROOT = os.path.join(ROOT_DIR, "media")
    if not os.path.exists(MEDIA_ROOT):
        os.mkdir(MEDIA_ROOT)

# #####################
#   APPS & MIDDLEWARE
# #####################

INSTALLED_APPS = [
{%- if cookiecutter.cms == "wagtail" %}
    "{{ cookiecutter.site_app }}.home",
    "{{ cookiecutter.site_app }}.search",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "modelcluster",
    "taggit",
{%- endif %}
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
{%- if cookiecutter.use_celery == "y" %}
    "django_celery_beat",
{%- endif %}
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
{%- if cookiecutter.cms == "wagtail" %}
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
{%- endif %}
{%- if cookiecutter.use_structlog == "y" %}
    "django_structlog.middlewares.RequestMiddleware",
    "django_structlog.middlewares.CeleryMiddleware",
{%- endif %}
]
{%- if cookiecutter.use_debug_toolbar == "y" %}

if ENV == "dev" and DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE
{%- endif %}



# ##############
#   WEB SERVER
# ##############

ROOT_URLCONF = "{{ cookiecutter.site_app }}.urls"

WSGI_APPLICATION = "{{ cookiecutter.site_app }}.wsgi.application"
{%- if cookiecutter.use_debug_toolbar == "y" %}

if ENV == "dev":
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
{%- endif %}


# ############
#   DATABASE
# ############

if ENV == "dev":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(ROOT_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ["DB_NAME"],
            "USER": os.environ["DB_USER"],
            "PASSWORD": os.environ["DB_PASSWORD"],
            "HOST": os.environ["DB_HOST"],
            "PORT": os.environ["DB_PORT"],
        }
    }


# ###########
#   CACHING
# ###########

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "site",
    }
}


# ############
#   SECURITY
# ############

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = get_env_list("ALLOWED_HOSTS")

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]


# #############
#   TEMPLATES
# #############

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(ROOT_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ########################
#   INTERNATIONALIZATION
# ########################

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    os.path.join(ROOT_DIR, "locale"),
]


# ################
#   STATIC FILES
# ################

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(ROOT_DIR, 'static'),
]

if ENV in ("prod", "staging"):
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# ###########
#   LOGGING
# ###########

LOG_FORMATTER = os.environ["LOG_FORMATTER"]
LOG_LEVEL = os.environ["LOG_LEVEL"]

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
{%- if cookiecutter.use_structlog == "y" %}
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "key_value": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=["timestamp", "level", "event", "logger"]
            ),
        },
        "console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
{%- else %}
        "console": {
            "format": "[%(asctime)s|%(levelname)s|%(name)s.%(funcName)s|%(lineno)s] %(message)s",
        },
{%- endif %}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": os.environ["LOG_FORMATTER"],
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console"],
        },
        "django": {
            "level": "ERROR",
            "propagate": True,
        },
{% if cookiecutter.use_celery == "y" %}
        "celery": {
            "level": "ERROR",
            "propagate": True,
        },
{%- endif %}
        "{{ cookiecutter.site_app }}": {
            "level": LOG_LEVEL,
            "propagate": True,
        },
    },
})
{%- if cookiecutter.use_structlog == "y" %}

# noinspection DuplicatedCode
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,  # noqa
    cache_logger_on_first_use=True,
)
{%- endif %}
{%- if cookiecutter.use_sentry %}


# ##########
#   SENTRY
# ##########

if get_env_boolean("SENTRY_ENABLED", True):
    import sentry_sdk
{%- if cookiecutter.use_celery == "y" %}
    from sentry_sdk.integrations.celery import CeleryIntegration
{%- endif %}
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        os.environ["SENTRY_DSN"],
        integrations=[
            DjangoIntegration(),
{%- if cookiecutter.use_celery == "y" %}
            CeleryIntegration(),
{%- endif %}
        ]
    )
{%- endif %}


# #########
#   EMAIL
# #########

if ENV == "prod":
    EMAIL_HOST = os.environ["EMAIL_HOST"]
    EMAIL_PORT = os.environ["EMAIL_PORT"]
    EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
    EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
    EMAIL_USE_TLS = get_env_boolean("EMAIL_USE_TLS")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]
{%- if cookiecutter.cms == "wagtail" %}


# ###########
#   WAGTAIL
# ###########

WAGTAIL_SITE_NAME = "{{ cookiecutter.site_app }}"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'
{%- endif %}
