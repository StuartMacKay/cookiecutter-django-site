{%- if cookiecutter.use_structlog == "y" %}
import logging
{%- endif %}
import os
{%- if cookiecutter.use_structlog == "y" %}

import structlog
{%- endif %}
from celery import Celery
from celery.schedules import crontab
{%- if cookiecutter.use_structlog == "y" %}
from celery.signals import setup_logging
from django_structlog.celery.steps import DjangoStructLogInitStep
{%- endif %}


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ cookiecutter.site_app }}.settings')

app = Celery('{{ cookiecutter.site_app }}')

app.config_from_object("{{ cookiecutter.site_app }}.celeryconfig")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
#    'sample_task': {
#        'task': '{{ cookiecutter.site_app }}.tasks.sample_task',
#        'schedule': crontab(minute='0'),
#        'args': (),
#    },
}
{%- if cookiecutter.use_structlog == "y" %}


LOG_FORMATTER = os.environ["LOG_FORMATTER"]
LOG_LEVEL = os.environ["LOG_LEVEL"]


@setup_logging.connect
def receiver_setup_logging(loglevel, logfile, format, colorize, **kwargs):  # noqa

    logging.config.dictConfig(  # noqa
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
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
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": LOG_FORMATTER,
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
                "celery": {
                    "level": "INFO",
                    "propagate": True,
                },
                "newsdesk": {
                    "level": LOG_LEVEL,
                    "propagate": True,
                },
            },
        }
    )

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
