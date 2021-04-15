import math
import os
import traceback

import xarray as xr

from roocs_utils import CONFIG
from roocs_utils.catalog_maker import logging
from roocs_utils.catalog_maker.catalog import create_catalog
from roocs_utils.catalog_maker.catalog import get_files
from roocs_utils.catalog_maker.utils import get_pickle_store
from roocs_utils.catalog_maker.utils import get_var_id

LOGGER = logging.getLogger(__file__)


class Scanner(object):
    def __init__(self, batch, project):
        self._batch = batch
        self._project = project

        self._config = CONFIG[f"project:{project}"]
        self._catalog_pickle = get_pickle_store("catalog", self._project)
        self._error_pickle = get_pickle_store("error", self._project)

    def _id_to_directory(self, dataset_id):
        archive_dir = self._config["archive_dir"]
        return os.path.join(archive_dir, dataset_id.replace(".", "/"))

    def scan(self, dataset_id):
        fpaths = get_files(dataset_id)

        for fpath in fpaths:
            # Clear out error state if previously recorded
            self._error_pickle.clear(fpath)

            if self._catalog_pickle.contains(fpath):
                LOGGER.info(f"Already converted to catalog: {fpath}")
                return

            LOGGER.info(f"Scanning file: {fpath}")

            try:
                content = create_catalog(self._project, dataset_id, fpath)

            except Exception:
                msg = f"Failed to extract content for: {fpath}"
                return self._wrap_exception(fpath, msg)

            try:
                self._finalise(fpath, content)
                LOGGER.info(f"Finalised: {fpath}")

            except Exception:
                msg = f"Finalisation failed for: {fpath}"
                self._wrap_exception(fpath, msg)

    def _finalise(self, fpath, content):
        self._catalog_pickle.add(fpath, content)
        LOGGER.info(f"Wrote pickle entries for: {fpath}")

    def _wrap_exception(self, fpath, msg):
        tb = traceback.format_exc()
        error = f"{msg}:\n{tb}"
        self._error_pickle.add(fpath, error)
        LOGGER.error(f"FAILED TO COMPLETE FOR: {fpath}\n{error}")
