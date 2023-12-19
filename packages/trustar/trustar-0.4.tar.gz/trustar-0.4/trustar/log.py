"""
Setups TruSTAR SDK v1 logger
"""
# ! /usr/local/bin/python3

# Available objects from log: get_logger and TrustarJSONFormatter
__all__ = ["get_logger", "TrustarJSONFormatter"]

import datetime
import logging
import logging.handlers
import os
import sys

import json_log_formatter

from .config import (
    LOGGING_LEVEL_VAR,
    LOGGING_FILENAME_VAR,
    LOGGING_STDOUT_ENABLED_VAR,
)

DEFAULT_LOGGING_LEVEL = logging.INFO


class TrustarJSONFormatter(json_log_formatter.JSONFormatter):
    """
    Custom class to override default JSONFormatter
    """

    def format(self, record):
        """
            Default behaviour of JSONFormatter is to cast everything into a string.
            Avoiding to call 'getMessage' method, and leaves the object as it is,
            this way json messages can have nested objects
        """
        message = record.msg
        extra = self.extra_from_record(record)
        json_record = self.json_record(message, extra, record)
        mutated_record = self.mutate_json_record(json_record)
        # Backwards compatibility: Functions that overwrite this but don't
        # return a new value return None because they modified the
        # argument passed in.
        if mutated_record is None:
            mutated_record = json_record

        return self.to_json(mutated_record)

    def json_record(self, message, extra, record):
        """
            Updates extra attributes from record
        """
        extra = {
            'message': message,
            'level': record.levelname,
            'module': record.name,
            'time': datetime.datetime.utcnow()
        }

        if record.exc_info:
            extra['exec_info'] = self.formatException(record.exc_info)

        return extra

    def to_json(self, record):
        """
            Converts record dict to a JSON string.

            Best effort to serialize a record (represents an object as a string)
            instead of raising TypeError if json library supports default argument.
        """
        return self.json_lib.dumps(record, default=_json_object_encoder)


def _json_object_encoder(obj):
    """
        Sugarcoats serializing obj into JSON

    :param obj: Python obj to be serialized

    :return: JSON representation from obj
    """
    try:
        return obj.to_json()
    except AttributeError:
        return f"{obj}"

def get_stdout_handler(formatter):
    """
    Gets the handler to manage the output of the logger, default: stdout
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    return handler

def get_file_handler(filename, formatter):
    """
    Gets the file handler to manage the output of the logger as instances of
    filenames, e.g. [filename.log0, filename.log1, ..., filename.log9]
    """
    handler = logging.handlers.RotatingFileHandler(
        filename=filename,
        mode='a',
        maxBytes=8192000,
        backupCount=10,
    )
    handler.setFormatter(formatter)

    return handler

def get_log_file(filename=None):
    """
        Returns the log file 'filename' if it is set.
        By default also creates the file, if it does not exist.
    """
    filename = filename or os.environ.get(LOGGING_FILENAME_VAR)
    if not filename:
        return None

    with open(filename, "a+"):
        return filename


def get_formatter():
    """
        Creates a TrustarJSONFormatter formater.
    """
    return TrustarJSONFormatter()


def get_logger(
                name=None,
                filename=None,
                stdout_enabled=True,
                level=None
            ):
    """
        Creates a custom logger for given configuration.
    """
    logger = logging.getLogger(name or __name__)
    outoput_formatter = get_formatter()

    stdout_enabled = stdout_enabled and int(os.environ.get(LOGGING_STDOUT_ENABLED_VAR, 1))
    if stdout_enabled:
        stdout_handler = get_stdout_handler(formatter=outoput_formatter)
        logger.addHandler(stdout_handler)

    file = get_log_file(filename)
    if file:
        file_handler = get_file_handler(file, formatter=outoput_formatter)
        logger.addHandler(file_handler)

    level = level or int(os.environ.get(LOGGING_LEVEL_VAR, DEFAULT_LOGGING_LEVEL))
    logger.setLevel(level)

    return logger
