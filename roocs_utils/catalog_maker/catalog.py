import glob
import os
import sys
import time
from collections import OrderedDict
from datetime import datetime

import numpy as np
import pandas as pd
import xarray as xr
import yaml

from roocs_utils import CONFIG
from roocs_utils.catalog_maker.utils import create_dir
from roocs_utils.project_utils import DatasetMapper
from roocs_utils.xarray_utils.xarray_utils import get_coord_type
from roocs_utils.xarray_utils.xarray_utils import open_xr_dataset


def get_time_info(fpath, var_id):
    all_times = []
    try:

        ds = xr.open_dataset(fpath, use_cftime=True)
        times = ds[var_id].time.values

        all_times.extend(list(times))
        ds.close()
    except AttributeError:
        return 0, "undefined"

    return (
        len(all_times),
        all_times[0].isoformat(timespec="seconds"),
        all_times[-1].isoformat(timespec="seconds"),
    )


def get_coord_info(fpaths):
    ds = open_xr_dataset(fpaths)

    d = OrderedDict()

    for coord_id in sorted(ds.coords):

        coord = ds.coords[coord_id]
        coord_type = get_coord_type(coord)

        if coord_type == "time" or coord_type is None:
            continue

        data = coord.values

        mn, mx = data.min(), data.max()

        if np.isnan(mn) or np.isnan(mx):
            mn, mx = float(coord.min()), float(coord.max())

        if coord_type == "longitude":
            if mn < -360 or mx > 360:
                raise Exception(
                    f"Longitude is not within expected bounds. The minimum and maximum are {mn}, {mx}"
                )

        if coord_type == "latitude":
            if mn < -90 or mx > 90:
                raise Exception(
                    f"Latitude is not within expected bounds. The minimum and maximum are {mn}, {mx}"
                )

        d[f"{coord_type}"] = f"{mn:.2f} {mx:.2f}"

    return d


def get_size_data(fpath):
    ds = open_xr_dataset(fpath)

    size = ds.nbytes
    size_gb = round(size / 1e9, 2)

    return size, size_gb


def get_files(ds_id):
    fpaths = DatasetMapper(ds_id).files

    if len(fpaths) < 1:
        raise FileNotFoundError("No files were found for this dataset")

    return fpaths


def get_var_metadata(fpath, var_id):
    time_length, start_time, end_time = get_time_info(fpath, var_id)
    time_string = start_time + " " + end_time

    print(f"[INFO] Reading {fpath}")

    ds = open_xr_dataset(fpath)
    dims = ds[var_id].dims

    shape_annotated = []

    for i in range(len(dims)):
        dim = dims[i]
        length = ds[var_id].shape[i]

        if dim.startswith("time"):
            item = str(time_string)
        else:
            item = str(length)

        shape_annotated.append(item)

    dims = " ".join(list(dims))
    shape = " ".join(list(shape_annotated))

    ds.close()

    return dims, shape, start_time, end_time


def build_dict(ds_id, fpath, proj_dict):

    comps = ds_id.split(".")

    facet_rule = proj_dict["facet_rule"]
    facets = dict([_ for _ in zip(facet_rule, comps)])

    var_id = facets.get("variable") or facets.get("variable_id")

    size, size_gb = get_size_data(fpath)
    dims, shape, start_time, end_time = get_var_metadata(fpath, var_id)
    coord_d = get_coord_info(fpath)

    d = OrderedDict()

    d["ds_id"] = ds_id
    d["path"] = "/".join(ds_id.split(".")[1:]) + fpath.split("/")[-1]

    d["size"] = size
    d["size_gb"] = size_gb

    d.update(facets)

    d["start_time"] = start_time
    d["end_time"] = end_time
    d.update(coord_d)

    return d


def create_catalog(project, ds_id, fpath):
    proj_dict = CONFIG[f"project:{project}"]
    d = build_dict(ds_id, fpath, proj_dict)
    return d


def write_catalog(df, project, last_updated, cat_dir, compress):
    version_stamp = last_updated.strftime("v%Y%m%d")
    cat_name = f"{project}_{version_stamp}.csv"
    if compress:
        cat_name += ".gz"
        compression = "gzip"
    else:
        compression = None
    cat_path = os.path.join(cat_dir, cat_name)
    df.to_csv(cat_path, index=False, compression=compression)
    return cat_path


def update_catalog(project, path, last_updated, cat_dir):
    cat_name = f"{project}.yml"
    cat_path = os.path.join(cat_dir, cat_name)

    try:
        with open(cat_path) as fin:
            cat = yaml.load(fin, Loader=yaml.SafeLoader)
            cat["sources"][project]["args"][
                "urlpath"
            ] = "{{ CATALOG_DIR }}/" + os.path.basename(path)
            timestamp = last_updated.strftime("%Y-%m-%dT%H:%M:%SZ")
            cat["sources"][project]["metadata"]["last_updated"] = timestamp
            with open(cat_path, "w") as fout:
                yaml.dump(cat, fout)
        return cat_path
    except FileNotFoundError:
        raise Exception(
            f"Yaml catalog descriptor does not exist yet, create file {cat_path} based on "
            "the template described in the readme."
        )


def to_csv(content, project):
    # create the dataframe

    df = pd.DataFrame(content)
    # write catalog
    cat_dir = CONFIG[f"project:{project}"]["catalog_dir"]
    create_dir(cat_dir)

    last_updated = datetime.now().utcnow()
    cat_path = write_catalog(
        df,
        project,
        last_updated,
        cat_dir,
        compress=False,
    )
    print(f"Catalog written {cat_path}")
    return cat_path, last_updated