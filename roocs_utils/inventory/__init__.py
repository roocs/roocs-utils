import logging
import os

from roocs_utils import CONFIG

LOG_LEVEL = "INFO"
logging.basicConfig(level=LOG_LEVEL)


for env_var, value in CONFIG["environment"].items():
    os.environ[env_var.upper()] = value
