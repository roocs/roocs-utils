from datetime import datetime

import numpy as np
import xarray as xr
from cfunits import Units


known_coord_types = [
    'time', 'level', 'latitude', 'longitude'
]


# from dachar
def get_coord_by_attr(ds, attr, value):
    coords = ds.coords

    for coord in coords.values():
        if coord.attrs.get(attr, None) == value:
            return coord

    return None


def is_latitude(coord):
    if hasattr(coord, "units"):
        if Units(coord.units).islatitude:
            return True

    elif coord.attrs.get("standard_name", None) == "latitude":
        return True


def is_longitude(coord):
    if hasattr(coord, "units"):
        if Units(coord.units).islongitude:
            return True

    elif coord.attrs.get("standard_name", None) == "longitude":
        return True


def is_level(coord):
    if hasattr(coord, "units"):
        if Units(coord.units).ispressure:
            return True

    if hasattr(coord, "positive"):
        if coord.attrs.get("positive", None) == "up" or "down":
            return True

    if hasattr(coord, "axis"):
        if coord.attrs.get("axis", None) == "Z":
            return True


def is_time(coord):
    if coord.values.size > 1:
        if hasattr(coord.values[0], "calendar"):
            if Units(calendar=coord.values[0].calendar).isreftime:
                return True

    elif hasattr(coord, "axis"):
        if coord.axis == "T":
            return True

    elif coord.attrs.get("standard_name", None) == "time":
        return True


def get_coord_type(coord):

    if is_longitude(coord):
        return "longitude"
    elif is_latitude(coord):
        return "latitude"
    elif is_level(coord):
        return "level"
    elif is_time(coord):
        return "time"

    return None


def get_coord_by_type(ds, coord_type, ignore_aux_coords=True):
    'Can take a Dataset or DataArray'
    if coord_type not in known_coord_types:
        raise Exception(f'Coordinate type not known: {coord_type}')

    for coord_id in ds.coords:
        # If ignore_aux_coords is True then ignore coords that are not dimensions
        if ignore_aux_coords and coord_id not in ds.dims:
            continue

        coord = ds.coords[coord_id]

        if get_coord_type(coord) == coord_type:
            return coord

    return None


def get_main_variable(ds, exclude_common_coords=True):

    data_dims = [data.dims for var_id, data in ds.variables.items()]
    flat_dims = [dim for sublist in data_dims for dim in sublist]

    results = {}
    common_coords = ["bnd", "bound", "lat", "lon", "time", "level"]

    for var_id, data in ds.variables.items():

        if var_id in flat_dims:
            continue
        if exclude_common_coords is True and any(coord in var_id for coord in common_coords):
            continue
        else:
            results.update({var_id: len(ds[var_id].shape)})
    result = max(results, key=results.get)

    if result is None:
        raise Exception("Could not determine main variable")
    else:
        return result
