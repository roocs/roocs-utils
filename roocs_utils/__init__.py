"""Top-level package for roocs-utils."""

__author__ = """Eleanor Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
__version__ = "0.6.9"

from roocs_utils.config import get_config
import roocs_utils

CONFIG = get_config()

from .parameter import *
from .xarray_utils import *
from .utils import *

import logging
import os


for env_var, value in CONFIG["environment"].items():
    os.environ[env_var.upper()] = value
