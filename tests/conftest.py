import os
from pathlib import Path
import pytest
import shutil

MINI_ESGF_CACHE_DIR = Path.home() / ".mini-esgf-data"
TEST_DATA_REPO_URL = 'https://github.com/roocs/mini-esgf-data'

CMIP5_TAS = os.path.join(
    MINI_ESGF_CACHE_DIR,
    'master/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc'
)

CMIP5_ZOSTOGA = os.path.join(
    MINI_ESGF_CACHE_DIR,
    'master/test_data/badc/cmip5/data/cmip5/output1/INM/inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/zostoga_Omon_inmcm4_rcp45_r1i1p1_200601-210012.nc'
)

CMIP6_SICONC = os.path.join(
    MINI_ESGF_CACHE_DIR,
    'master/test_data/badc/cmip6/data/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/SImon/siconc/gn/latest/siconc_SImon_CanESM5_historical_r1i1p1f1_gn_185001-201412.nc'
)

C3S_CMIP5_TAS = os.path.join(
    MINI_ESGF_CACHE_DIR,
    'master/test_data/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/ICHEC/EC-EARTH/historical/day/atmos/day/r1i1p1/tas/v20131231/*nc'
)


@pytest.fixture
def load_test_data():
    """
    This fixture ensures that the required test data repository
    has been cloned to the cache directory within the home directory.
    """
    tmp_repo = '/tmp/.mini-esgf-data'
    test_data_dir = os.path.join(tmp_repo, 'test_data')
    target = os.path.join(MINI_ESGF_CACHE_DIR, 'master')

    if not os.path.isdir(target):

        os.makedirs(target) 
        os.system(f'git clone {TEST_DATA_REPO_URL} {tmp_repo}')

        shutil.move(test_data_dir, target)
        shutil.rmtree(tmp_repo)  
