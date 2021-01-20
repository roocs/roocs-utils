import os

import xarray as xr

from roocs_utils.xarray_utils.xarray_utils import open_xr_dataset
from tests.conftest import C3S_CMIP5_TAS


def test_open_xr_dataset():
    dset = C3S_CMIP5_TAS
    ds_id = open_xr_dataset(dset)

    assert isinstance(ds_id, xr.Dataset)
