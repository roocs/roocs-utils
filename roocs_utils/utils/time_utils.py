import numpy as np


def to_isoformat(tm):
    """Returns an ISO 8601 string from a time object (of different types)."""
    if type(tm) == np.datetime64:
        return str(tm).split(".")[0]
    else:
        return tm.isoformat()
