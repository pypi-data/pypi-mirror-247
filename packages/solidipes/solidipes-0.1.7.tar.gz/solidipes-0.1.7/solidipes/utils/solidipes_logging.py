#!/usr/bin/env python

import logging
import os
import sys

from .utils import get_study_log_path

# Base level logger
root_logger = logging.getLogger("solidipes")
root_logger.propagate = True
root_logger.setLevel(logging.DEBUG)  # Avoid hard-filtering

# Logging format
SOLIDIPES_FORMAT = "%(levelname)s: %(message)s"

if "FULL_SOLIDIPES_LOG" in os.environ:
    SOLIDIPES_FORMAT = "%(pathname)s:%(lineno)d:%(levelname)s: %(message)s"
formatter_sh = logging.Formatter(SOLIDIPES_FORMAT)
SOLIDIPES_FORMAT = "%(asctime)s %(filename)s:%(lineno)d %(levelname)s: %(message)s"
formatter_file = logging.Formatter(SOLIDIPES_FORMAT)

sh = logging.StreamHandler(sys.stderr)
if "FULL_SOLIDIPES_LOG" not in os.environ:
    sh.setLevel(logging.INFO)  # Only show info
else:
    sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter_sh)
root_logger.addHandler(sh)

try:
    log_filename = get_study_log_path()
    file_handler = logging.FileHandler(log_filename, mode="a+")
    file_handler.setLevel(logging.DEBUG)  # Log everything to file
    file_handler.setFormatter(formatter_file)

    root_logger.addHandler(file_handler)
    root_logger.info("Activated logging to file")

except FileNotFoundError:
    root_logger.error("Cannot activate logging to file")


def getLogger():
    return logging.getLogger("solidipes")


def invalidPrint(x):
    raise Exception('print should not be used in that class: use the logging system instead: "{0}"'.format(x))
