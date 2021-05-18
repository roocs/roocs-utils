import json
import os
import uuid

import xarray as xr

from roocs_utils import CONFIG


def get_var_id(dataset_id, project):
    var_index = CONFIG[f"project:{project}"]["var_index"]
    return dataset_id.split(".")[var_index]


def create_dir(dr):
    if not os.path.isdir(dr):
        os.makedirs(dr)


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
