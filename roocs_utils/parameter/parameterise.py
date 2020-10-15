import xarray as xr

from roocs_utils.parameter import area_parameter
from roocs_utils.parameter import collection_parameter
from roocs_utils.parameter import level_parameter
from roocs_utils.parameter import time_parameter


def parameterise(collection=None, area=None, level=None, time=None):
    """
    Parameterises inputs to instances of parameter classes which allows
    them to be used throughout roocs.
    For supported formats for each input please see their individual classes.

    :param collection: Collection input in any supported format.
    :param area: Area input in any supported format.
    :param level: Level input in any supported format.
    :param time: Time input in any supported format.
    :return: Parameters as instances of their respective classes.
    """

    # if collection is a dataset/dataarray it doesn't need to be parameterised
    if type(collection) not in (xr.core.dataarray.DataArray, xr.core.dataset.Dataset):
        collection = collection_parameter.CollectionParameter(collection)

    area = area_parameter.AreaParameter(area)
    time = time_parameter.TimeParameter(time)
    level = level_parameter.LevelParameter(level)

    return locals()
