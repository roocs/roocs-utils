import os
from datetime import datetime
from pathlib import Path

import cf_xarray  # noqa
import cftime
import numpy as np
import xarray as xr

from roocs_utils.project_utils import dset_to_filepaths

known_coord_types = ["time", "level", "latitude", "longitude"]


def open_xr_dataset(dset):
    """
    Opens an xarray dataset from a dataset input.

    :param dset: (Str or Path) ds_id, directory path or file path ending in *.nc.
    Any list will be interpreted as list of files
    """

    # DatasetMapper doesn't handle lists
    if not isinstance(dset, list):
        # use force=True to allow all file paths to pass through DatasetMapper
        dset = dset_to_filepaths(dset, force=True)

    # if a list we want a multi-file dataset
    if len(dset) > 1:
        return xr.open_mfdataset(dset, use_cftime=True, combine="by_coords")
    # if there is only one file we only need to call open_dataset
    else:
        return xr.open_dataset(dset[0], use_cftime=True)


# from dachar
def get_coord_by_attr(ds, attr, value):
    """
    Returns a coordinate based on a known attribute of a coordinate.

    :param ds: Xarray Dataset or DataArray
    :param attr: (str) Name of attribute to look for.
    :param value: Expected value of attribute you are looking for.
    :return: Coordinate of xarray dataset if found.
    """
    coords = ds.coords

    for coord in coords.values():
        if coord.attrs.get(attr, None) == value:
            return coord

    return None


def is_latitude(coord):
    """
    Determines if a coordinate is latitude.

    :param coord: coordinate of xarray dataset e.g. coord = ds.coords[coord_id]
    :return: (bool) True if the coordinate is latitude.
    """
    if "latitude" in coord.cf and coord.cf["latitude"].name == coord.name:
        return True

    if coord.attrs.get("standard_name", None) == "latitude":
        return True

    return False


def is_longitude(coord):
    """
    Determines if a coordinate is longitude.

    :param coord: coordinate of xarray dataset e.g. coord = ds.coords[coord_id]
    :return: (bool) True if the coordinate is longitude.
    """
    if "longitude" in coord.cf and coord.cf["longitude"].name == coord.name:
        return True

    if coord.attrs.get("standard_name", None) == "longitude":
        return True

    return False


def is_level(coord):
    """
    Determines if a coordinate is level.

    :param coord: coordinate of xarray dataset e.g. coord = ds.coords[coord_id]
    :return: (bool) True if the coordinate is level.
    """
    if "vertical" in coord.cf and coord.cf["vertical"].name == coord.name:
        return True

    if hasattr(coord, "positive"):
        if coord.attrs.get("positive", None) == "up" or "down":
            return True

    if hasattr(coord, "axis"):
        if coord.attrs.get("axis", None) == "Z":
            return True

    return False


def is_time(coord):
    """
    Determines if a coordinate is time.

    :param coord: coordinate of xarray dataset e.g. coord = ds.coords[coord_id]
    :return: (bool) True if the coordinate is time.
    """
    if "time" in coord.cf and coord.cf["time"].name == coord.name:
        return True

    if np.issubdtype(coord.dtype, np.datetime64):
        return True

    if isinstance(np.atleast_1d(coord.values)[0], cftime.datetime):
        return True

    if hasattr(coord, "axis"):
        if coord.axis == "T":
            return True

    if coord.attrs.get("standard_name", None) == "time":
        return True

    return False


def get_coord_type(coord):
    """
    Gets the coordinate type.

    :param coord: coordinate of xarray dataset e.g. coord = ds.coords[coord_id]
    :return: The type of coordinate as a string. Either longitude, latitude, time, level or None
    """

    if is_longitude(coord):
        return "longitude"
    elif is_latitude(coord):
        return "latitude"
    elif is_level(coord):
        return "level"
    elif is_time(coord):
        return "time"

    return None


def convert_coord_to_axis(coord):
    """
    Converts coordinate type to its single character axis identifier (tzyx).

    :param coord: (str) The coordinate to convert.
    :return: (str) The single character axis identifier of the coordinate (tzyx).
    """

    axis_dict = {"time": "t", "longitude": "x", "latitude": "y", "level": "z"}
    return axis_dict.get(coord, None)


def get_coord_by_type(ds, coord_type, ignore_aux_coords=True):
    """
    Returns the xarray Dataset or DataArray coordinate of the specified type.

    :param ds: Xarray Dataset or DataArray
    :param coord_type: (str) Coordinate type to find.
    :param ignore_aux_coords: (bool) If True then coordinates that are not dimensions are ignored.
                            Default is True.
    :return: Xarray Dataset coordinate (ds.coords[coord_id])
    """
    "Can take a Dataset or DataArray"

    if coord_type not in known_coord_types:
        raise Exception(f"Coordinate type not known: {coord_type}")

    for coord_id in ds.coords:
        # If ignore_aux_coords is True then ignore coords that are not dimensions
        if ignore_aux_coords and coord_id not in ds.dims:
            continue

        coord = ds.coords[coord_id]

        if get_coord_type(coord) == coord_type:
            return coord

    return None


def get_main_variable(ds, exclude_common_coords=True):
    """
    Finds the main variable of an xarray Dataset

    :param ds: xarray Dataset
    :param exclude_common_coords: (bool) If True then common coordinates are excluded from the search for the
                                main variable. common coordinates are time, level, latitude, longitude and bounds.
                                Default is True.
    :return: (str) The main variable of the dataset e.g. 'tas'
    """

    data_dims = [data.dims for var_id, data in ds.variables.items()]
    flat_dims = [dim for sublist in data_dims for dim in sublist]

    results = {}
    common_coords = ["bnd", "bound", "lat", "lon", "time", "level"]

    for var_id, data in ds.variables.items():

        if var_id in flat_dims:
            continue
        if exclude_common_coords is True and any(
            coord in var_id for coord in common_coords
        ):
            continue
        else:
            results.update({var_id: len(ds[var_id].shape)})
    result = max(results, key=results.get)

    if result is None:
        raise Exception("Could not determine main variable")
    else:
        return result
