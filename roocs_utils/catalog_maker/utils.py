import json
import os
import uuid

import xarray as xr

from roocs_utils import CONFIG
from roocs_utils.inventory.pickle_store import PickleStore

known_pickles = ["inventory", "error"]


def get_var_id(dataset_id, project):
    var_index = CONFIG[f"project:{project}"]["var_index"]
    return dataset_id.split(".")[var_index]


def create_dir(dr):
    if not os.path.isdir(dr):
        os.makedirs(dr)


def get_pickle_store(store_type, project):
    """
    Return a pickle store of type: `store_type`.
    Pickle store types can be any listed in: `known_pickles`

    Args:
        store_type ([string]): pickle type
        project ([string]): project
    """
    if store_type not in known_pickles:
        raise KeyError(f"Pickle store type not known: {store_type}")

    _config = CONFIG[f"project:{project}"]
    return PickleStore(_config[f"{store_type}_pickle"])


def to_dataset_id(path, project):
    items = path.replace("/", ".").split(".")
    if items[-1].endswith(".nc") or items[-1] == "zarr":
        items = items[:-1]

    n_facets = CONFIG[f"project:{project}"]["n_facets"]
    return ".".join(items[-n_facets:])


def get_archive_path(path, project):
    dataset_id = to_dataset_id(path)
    archive_dir = CONFIG[f"project:{project}"]["archive_dir"]

    return os.path.join(archive_dir, dataset_id.replace(".", "/"))
