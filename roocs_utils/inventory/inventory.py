import glob
import os
import sys
import time
from collections import OrderedDict

import oyaml
import xarray as xr

from roocs_utils import CONFIG
from roocs_utils.xarray_utils.xarray_utils import get_coord_type


def get_time_info(fpaths, var_id):

    all_times = []
    for fpath in sorted(fpaths):

        try:
            ds = xr.open_dataset(fpath, use_cftime=True)
            times = ds[var_id].time.values

            all_times.extend(list(times))
            ds.close()
        except AttributeError:
            return 0, None

    return len(all_times), all_times[0].isoformat() + " " + all_times[-1].isoformat()


def get_coord_info(fpaths):
    ds = xr.open_mfdataset(fpaths, use_cftime=True, combine="by_coords")

    d = OrderedDict()

    for coord_id in sorted(ds.coords):

        coord = ds.coords[coord_id]
        type = get_coord_type(coord)

        if type == "time" or type is None:
            continue

        data = coord.values

        mn, mx = data.min(), data.max()

        d[f"{type}"] = f"{mn:.2f} {mx:.2f}"

    return d


def get_size_data(fpaths):
    files = len(fpaths)

    ds = xr.open_mfdataset(fpaths, use_cftime=True, combine="by_coords")

    size = ds.nbytes
    size_gb = round(size / 1e9, 2)

    return size, size_gb, files


def get_var_metadata(fpaths, var_id):

    time_length, time_string = get_time_info(fpaths, var_id)

    f1 = fpaths[0]
    print(f"[INFO] Reading {f1}")

    ds = xr.open_dataset(f1, use_cftime=True)
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


def build_dict(ds_id, proj_dict, base_dir):

    fpaths = glob.glob(base_dir + "/" + ds_id.replace(".", "/") + "/*.nc")

    comps = ds_id.split(".")

    facet_rule = proj_dict["facet_rule"]
    facets = dict([_ for _ in zip(facet_rule, comps)])

    var_id = facets.get("variable") or facets.get("variable_id")

    dims, shape, tm = get_var_metadata(fpaths, var_id)
    size, size_gb, files = get_size_data(fpaths)
    coord_d = get_coord_info(fpaths)
    fnames = [fpath.split("/")[-1] for fpath in fpaths]

    d = OrderedDict()
    d["path"] = ds_id.replace(".", "/")
    d["ds_id"] = ds_id
    d["var_id"] = var_id
    d["array_dims"] = dims
    d["array_shape"] = shape
    d["time"] = tm
    d.update(coord_d)
    d["size"] = size
    d["size_gb"] = size_gb
    d["file_count"] = files
    d["facets"] = facets
    d["files"] = fnames
    return d


def create_inventory(project, ds_id):
    proj_dict = CONFIG[f"project:{project}"]
    base_dir = proj_dict["base_dir"]
    d = build_dict(ds_id, proj_dict, base_dir)
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
