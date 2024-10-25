"""Top-level package for roocs-utils."""

import os
import warnings

from loguru import logger

from roocs_utils._version import __author__
from roocs_utils._version import __contact__
from roocs_utils._version import __copyright__
from roocs_utils._version import __license__
from roocs_utils._version import __version__
from roocs_utils.config import get_config


def showwarning(message, *args, **kwargs):
    """Inject warnings from `warnings.warn` into `loguru`."""
    logger.warning(message)
    showwarning_(message, *args, **kwargs)


showwarning_ = warnings.showwarning
warnings.showwarning = showwarning

# Disable logging for clisops and remove the logger that is instantiated on import
logger.disable("roocs_utils")
logger.remove()

CONFIG = get_config()

from roocs_utils.parameter import *
from roocs_utils.utils import *
from roocs_utils.xarray_utils import *

for env_var, value in CONFIG["environment"].items():
    os.environ[env_var.upper()] = value
