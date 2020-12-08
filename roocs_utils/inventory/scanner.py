import math
import os
import traceback

import xarray as xr

from roocs_utils import CONFIG
from roocs_utils.inventory import logging
from roocs_utils.inventory.inventory import create_inventory
from roocs_utils.inventory.utils import get_pickle_store
from roocs_utils.inventory.utils import get_var_id

LOGGER = logging.getLogger(__file__)


class Scanner(object):
    def __init__(self, batch, project):
        self._batch = batch
        self._project = project

        self._config = CONFIG[f"project:{project}"]
        self._inventory_pickle = get_pickle_store("inventory", self._project)
        self._error_pickle = get_pickle_store("error", self._project)

    def _id_to_directory(self, dataset_id):
        archive_dir = self._config["archive_dir"]
        return os.path.join(archive_dir, dataset_id.replace(".", "/"))

    def scan(self, dataset_id):
        # Clear out error state if previously recorded
        self._error_pickle.clear(dataset_id)

        if self._inventory_pickle.contains(dataset_id):
            LOGGER.info(f"Already converted to inventory: {dataset_id}")
            return

        LOGGER.info(f"Scanning dataset: {dataset_id}")

        try:
            content = create_inventory(self._project, dataset_id)
        except Exception:
            msg = f"Failed to extract content for: {dataset_id}"
            return self._wrap_exception(dataset_id, msg)

        try:
            self._finalise(dataset_id, content)
            LOGGER.info(f"Finalised: {dataset_id}")

        except Exception:
            msg = f"Finalisation failed for: {dataset_id}"
            self._wrap_exception(dataset_id, msg)

    def _finalise(self, dataset_id, content):
        self._inventory_pickle.add(dataset_id, content)
        LOGGER.info(f"Wrote pickle entries for: {dataset_id}")

    def _wrap_exception(self, dataset_id, msg):
        tb = traceback.format_exc()
        error = f"{msg}:\n{tb}"
        self._error_pickle.add(dataset_id, error)
        LOGGER.error(f"FAILED TO COMPLETE FOR: {dataset_id}\n{error}")
