from roocs_utils.parameter import (
    collection_parameter,
    area_parameter,
    time_parameter,
    level_parameter,
)


def parametrise_daops(collection=None, area=None, level=None, time=None):
    collection = collection_parameter.CollectionParameter(collection)
    area = area_parameter.AreaParameter(area)
    time = time_parameter.TimeParameter(time)
    level = level_parameter.LevelParameter(level)
    return collection.tuple, area.tuple, time.tuple, level.tuple


def parametrise_clisops(area=None, level=None, time=None):
    area = area_parameter.AreaParameter(area)
    time = time_parameter.TimeParameter(time)
    level = level_parameter.LevelParameter(level)
    return area.asdict(), time.asdict(), level.asdict()
