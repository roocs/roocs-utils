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
from roocs_utils.xarray_utils.xarray_utils import get_coord_by_type
from roocs_utils.xarray_utils.xarray_utils import open_xr_dataset


def get_time_info(ds, var_id):
    all_times = []
    try:

        times = ds[var_id].time.values

        all_times.extend(list(times))
        ds.close()
    except AttributeError:
        return "undefined", "undefined"

    return (
        all_times[0].isoformat(timespec="seconds"),
        all_times[-1].isoformat(timespec="seconds"),
    )


def get_coord_info(coord):
    data = coord.values

    mn, mx = data.min(), data.max()

    if np.isnan(mn) or np.isnan(mx):
        mn, mx = float(coord.min()), float(coord.max())

    return mn, mx


def get_bbox(ds):
    lat = get_coord_by_type(ds, "latitude", ignore_aux_coords=False)
    lon = get_coord_by_type(ds, "longitude", ignore_aux_coords=False)

    min_y, max_y = get_coord_info(lat)
    min_x, max_x = get_coord_info(lon)

    if min_y < -90 or max_y > 90:
        raise Exception(
            f"Latitude is not within expected bounds. The minimum and maximum are {min_y}, {max_y}"
        )

    if min_x < -360 or max_x > 360:
        raise Exception(
            f"Longitude is not within expected bounds. The minimum and maximum are {min_x}, {max_x}"
        )

    bbox = f"{min_x:.2f}, {min_y:.2f}, {max_x:.2f}, {max_y:.2f}"
    return bbox


def get_level_info(ds):
    coord = get_coord_by_type(ds, "level", ignore_aux_coords=False)

    if coord is not None:
        level_min, level_max = get_coord_info(coord)
        level = f"{level_min:.2f} {level_max:.2f}"

    else:
        level = " "

    return level


def get_size_data(fpath):

    # get file size
    size = os.path.getsize(fpath)
    size_gb = round(size / 1e9, 2)

    return size, size_gb


def get_files(ds_id):
    fpaths = DatasetMapper(ds_id).files

    if len(fpaths) < 1:
        raise FileNotFoundError("No files were found for this dataset")

    return fpaths


def build_dict(ds_id, fpath, proj_dict):
    comps = ds_id.split(".")
    ds = open_xr_dataset(fpath)

    facet_rule = proj_dict["facet_rule"]
    facets = dict([_ for _ in zip(facet_rule, comps)])

    var_id = facets.get("variable") or facets.get("variable_id")

    size, size_gb = get_size_data(fpath)
    start_time, end_time = get_time_info(ds, var_id)
    bbox = get_bbox(ds)
    level = get_level_info(ds)

    d = OrderedDict()

    d["ds_id"] = ds_id
    d["path"] = "/".join(ds_id.split(".")[1:]) + "/" + fpath.split("/")[-1]

    d["size"] = size
    # d["size_gb"] = size_gb

    d.update(facets)

    d["start_time"] = start_time
    d["end_time"] = end_time
    d["bbox"] = bbox
    d["level"] = level

    return d


def create_catalog(project, ds_id, fpath):
    proj_dict = CONFIG[f"project:{project}"]
    d = build_dict(ds_id, fpath, proj_dict)
    return d


def write_catalog(df, project, last_updated, csv_dir, compress):
    version_stamp = last_updated.strftime("v%Y%m%d")
    cat_name = f"{project}_{version_stamp}.csv"
    if compress:
        cat_name += ".gz"
        compression = "gzip"
    else:
        compression = None
    cat_path = os.path.join(csv_dir, cat_name)
    df.to_csv(cat_path, index=False, compression=compression)
    return cat_path


def update_catalog(project, path, last_updated, cat_dir):
    cat_name = "c3s.yaml"
    cat_path = os.path.join(cat_dir, cat_name)

    # dict to create yaml
    d = {
        f"{project}": {
            "description": f"{project} datasets",
            "driver": "intake.source.csv.CSVSource",
            "cache": [{"argkey": "urlpath", "type": "file"}],
            "args": {"urlpath": ""},
            "metadata": {"last_updated": ""},
        }
    }

    if not os.path.exists(cat_path):
        with open(cat_path, "w") as yaml_file:
            yaml.dump({"sources": d}, yaml_file, default_flow_style=False)

    with open(cat_path) as fin:
        cat = yaml.load(fin, Loader=yaml.SafeLoader)

        # check whether entry for project already exists
        try:
            cat["sources"][project]
        except KeyError:
            with open(cat_path, "a") as yaml_file:
                cat["sources"].update(d)
                yaml.dump(cat, yaml_file, default_flow_style=False)

    with open(cat_path) as fin:
        cat = yaml.load(fin, Loader=yaml.SafeLoader)
        cat["sources"][project]["args"][
            "urlpath"
        ] = "{{ CATALOG_DIR }}/" + os.path.relpath(path, start=cat_dir)
        timestamp = last_updated.strftime("%Y-%m-%dT%H:%M:%SZ")
        cat["sources"][project]["metadata"]["last_updated"] = timestamp
        with open(cat_path, "w") as fout:
            yaml.dump(cat, fout)

    return cat_path


def to_csv(content, project):
    # create the dataframe

    df = pd.DataFrame(content)
    # write catalog
    cat_dir = CONFIG[f"project:{project}"]["catalog_dir"]
    csv_dir = CONFIG[f"project:{project}"]["csv_dir"]

    # make sure directories exist
    create_dir(cat_dir)
    create_dir(csv_dir)

    last_updated = datetime.now().utcnow()
    cat_path = write_catalog(
        df,
        project,
        last_updated,
        csv_dir,
        compress=True,
    )
    print(f"Catalog written {cat_path}")
    return cat_path, last_updated
