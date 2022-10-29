from .settings import logstash_settings

LOG_DEFAULT_HANDLERS = [
    "console",
    "logstash",
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] [%(name)s]: %(message)s"
        },
        "logstash": {
            "()": "logstash_async.formatter.LogstashFormatter",
            "message_type": "recom-etl",
            "fqdn": False,
            "extra_prefix": "dev",
            "extra": {
                "environment": "production",
            },
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "logstash": {
            "level": "INFO",
            "class": "logstash_async.handler.AsynchronousLogstashHandler",
            "formatter": "logstash",
            "transport": "logstash_async.transport.UdpTransport",
            "host": logstash_settings.LOGSTASH_HOST,
            "port": logstash_settings.LOGSTASH_PORT,
            "ssl_enable": False,
            "ssl_verify": False,
            "database_path": "./logstash.db",
        },
    },
    "loggers": {
        "": {
            "handlers": LOG_DEFAULT_HANDLERS,
            "level": "INFO",
        },
    },
    "root": {
        "level": "INFO",
        "formatter": "default",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}
