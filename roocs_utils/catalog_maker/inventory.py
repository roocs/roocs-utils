import glob
import os
import sys
import time
from collections import OrderedDict

import numpy as np
import pandas as pd
import xarray as xr

from roocs_utils import CONFIG
from roocs_utils.project_utils import DatasetMapper
from roocs_utils.xarray_utils.xarray_utils import get_coord_type
from roocs_utils.xarray_utils.xarray_utils import open_xr_dataset


def get_time_info(fpaths, var_id):
    all_times = []
    for fpath in sorted(fpaths):

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


def get_size_data(fpaths):
    files = len(fpaths)

    ds = open_xr_dataset(fpaths)

    size = ds.nbytes
    size_gb = round(size / 1e9, 2)

    return size, size_gb, files


def get_var_metadata(fpaths, var_id):
    time_length, time_string = get_time_info(fpaths, var_id)

    f1 = fpaths[0]
    print(f"[INFO] Reading {f1}")

    ds = open_xr_dataset(f1)
    dims = ds[var_id].dims

    shape_annotated = []

    for i in range(len(dims)):
        dim = dims[i]
        length = ds[var_id].shape[i]

        if dim.startswith("time"):
            item = str(time_length)
        else:
            item = str(length)

        shape_annotated.append(item)

    dims = " ".join(list(dims))
    shape = " ".join(list(shape_annotated))

    ds.close()

    return dims, shape, time_string


def build_dicts(ds_id, proj_dict):
    fpaths = DatasetMapper(ds_id).files

    if len(fpaths) < 1:
        raise FileNotFoundError("No files were found for this dataset")

    comps = ds_id.split(".")

    facet_rule = proj_dict["facet_rule"]
    facets = dict([_ for _ in zip(facet_rule, comps)])

    var_id = facets.get("variable") or facets.get("variable_id")

    dims, shape, start_time, end_time = get_var_metadata(fpaths, var_id)
    size, size_gb, files = get_size_data(fpaths)
    coord_d = get_coord_info(fpaths)
    fnames = [fpath.split("/")[-1] for fpath in fpaths]
    dicts = []

    for fpath in fpaths:

        d = OrderedDict()

        d["ds_id"] = ds_id
        d["facets"] = facets

        d["start_time"] = start_time
        d["end_time"] = end_time
        d.update(coord_d)
        d["var_id"] = var_id
        d["array_dims"] = dims
        d["array_shape"] = shape
        d["size"] = size
        d["size_gb"] = size_gb
        d["file_count"] = files
        d["path"] = fpath

        dicts.append(d)

    return dicts


def create_inventory(project, ds_id):
    proj_dict = CONFIG[f"project:{project}"]
    d = build_dicts(ds_id, proj_dict)
    return d


def to_yaml(content, project, version):
    proj_dict = CONFIG[f"project:{project}"]
    base_dir = proj_dict["base_dir"]
    header = [{"project": project, "base_dir": base_dir}]

    if version == "c3s":
        inv_path = CONFIG[f"project:{project}"]["c3s_inventory_file"]
    else:
        inv_path = CONFIG[f"project:{project}"]["full_inventory_file"]

    if not os.path.isfile(inv_path):
        with open(inv_path, "w") as f:
            oyaml.dump(header, f)

    sdump = oyaml.dump(content, default_flow_style=False)

    with open(inv_path, "a") as f:
        f.write(sdump.replace("- path", "\n- path"))


def write_catalog(df, project, last_updated, compress):
    version_stamp = last_updated.strftime("v%Y%m%d")
    cat_name = f"{project}_{version_stamp}.csv"
    if compress:
        cat_name += ".gz"
        compression = "gzip"
    else:
        compression = None
    cat_path = here / "catalogs" / cat_name
    df.to_csv(cat_path, index=False, compression=compression)
    return cat_path


def update_catalog(project, path, origin, last_updated):
    cat_path = here / "catalogs" / "c3s.yaml"
    with open(cat_path) as fin:
        cat = yaml.load(fin, Loader=yaml.SafeLoader)
        cat["sources"][project]["args"]["urlpath"] = "{{ CATALOG_DIR }}/" + path.name
        timestamp = last_updated.strftime("%Y-%m-%dT%H:%M:%SZ")
        cat["sources"][project]["metadata"]["last_updated"] = timestamp
        cat["sources"][project]["metadata"]["origin_urlpath"] = origin
        with open(cat_path, "w") as fout:
            yaml.dump(cat, fout)
    return cat_path


def to_csv(content, project):
    # create the dataframe
    df = pd.DataFrame(content)
    # write catalog
    last_updated = datetime.now().utcnow()
    cat_path = write_catalog(df, project, last_updated, compress=True)
    print(f"Catalog written {cat_path}")
