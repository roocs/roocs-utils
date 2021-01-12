import os

import xarray as xr

from roocs_utils.xarray_utils.xarray_utils import open_xr_dataset
from tests._common import TESTS_HOME


def test_open_xr_dataset():
    dset = os.path.join(
        TESTS_HOME,
        "mini-esgf-data/test_data/gws/nopw/j04/cp4cds1_vol1/data/c3s-cmip5/output1/ICHEC"
        "/EC-EARTH/historical/day/atmos/day/r1i1p1/tas/v20131231/*.nc",
    )
    ds_id = open_xr_dataset(dset)

    assert ds_id == xr.open_mfdataset(
        os.path.join(
            TESTS_HOME,
            "mini-esgf-data/test_data/gws/nopw/j04/cp4cds1_vol1/data"
            "/c3s-cmip5/output1/ICHEC/EC-EARTH/historical/day/atmos/day"
            "/r1i1p1/tas/v20131231/*.nc",
        ),
        use_cftime=True,
        combine="by_coords",
    )
