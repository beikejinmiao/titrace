#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import logging
import logging.config
from conf.paths import LOG_FILEPATH


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": "true",
    "formatters": {
        "short": {
            "format": "%(asctime)s - %(levelname)s - %(message)s"
        },
        "default": {
            "class": "logging.Formatter",
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)s - %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": LOG_FILEPATH,
            "mode": "w+",
            "encoding": "utf-8"
        }
    },

    "loggers": {
        "console": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "file": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        }
    },

    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
}


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("file")
if not os.path.exists(LOG_FILEPATH):
    open(LOG_FILEPATH, 'a').close()

