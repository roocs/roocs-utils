# -*- coding: utf-8 -*-
"""Top-level package for roocs-utils."""

__author__ = """Eleanor Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
__version__ = "0.2.1"

from roocs_utils.config import get_config
import roocs_utils

CONFIG = get_config()

from .parameter import *
from .xarray_utils import *
from .utils import *
