import os
from pathlib import Path

import pytest
from _common import MINI_ESGF_CACHE_DIR
from _common import write_roocs_cfg
from git import Repo

write_roocs_cfg()

TEST_DATA_REPO_URL = "https://github.com/roocs/mini-esgf-data"

CMIP5_TAS = os.path.join(
    MINI_ESGF_CACHE_DIR,
    "master/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
)

CMIP5_TAS_EC_EARTH = os.path.join(
    MINI_ESGF_CACHE_DIR,
    "master/test_data/badc/cmip5/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
)

CMIP5_ZOSTOGA = os.path.join(
    MINI_ESGF_CACHE_DIR,
    "master/test_data/badc/cmip5/data/cmip5/output1/INM/inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/zostoga_Omon_inmcm4_rcp45_r1i1p1_200601-210012.nc",
)

CMIP6_SICONC = os.path.join(
    MINI_ESGF_CACHE_DIR,
    "master/test_data/badc/cmip6/data/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/SImon/siconc/gn/latest/siconc_SImon_CanESM5_historical_r1i1p1f1_gn_185001-201412.nc",
)

C3S_CMIP5_TAS = os.path.join(
    MINI_ESGF_CACHE_DIR,
    "master/test_data/gws/nopw/j04/cp4cds1_vol1/data/c3s-cmip5/output1/ICHEC/EC-EARTH/historical/day/atmos/day/r1i1p1/tas/v20131231/*.nc",
)

C3S_CORDEX_AFR_TAS = Path(
    MINI_ESGF_CACHE_DIR,
    "master/test_data/pool/data/CORDEX/data/cordex/output/AFR-22/GERICS/MPI-M-MPI-ESM-LR/historical/r1i1p1/GERICS-REMO2015/v1/day/tas/v20201015/*.nc",
).as_posix()

CMIP6_KERCHUNK_HTTPS_OPEN_JSON = (
    "https://gws-access.jasmin.ac.uk/public/cmip6_prep/eodh-eocis/kc-indexes-cmip6-http-v1/"
    "CMIP6.CMIP.MOHC.UKESM1-1-LL.1pctCO2.r1i1p1f2.Amon.tasmax.gn.v20220513.json"
)
CMIP6_KERCHUNK_HTTPS_OPEN_ZST = CMIP6_KERCHUNK_HTTPS_OPEN_JSON + ".zst"


@pytest.fixture
def cds_domain():
    return "https://data.mips.climate.copernicus.eu"


@pytest.fixture()
def cmip5_tas_ec_earth():
    return CMIP5_TAS_EC_EARTH


@pytest.fixture
def cmip5_zostoga():
    return CMIP5_ZOSTOGA


@pytest.fixture
def c3s_cmip5_tas():
    return C3S_CMIP5_TAS


@pytest.fixture
def c3s_cordex_afr_tas():
    return C3S_CORDEX_AFR_TAS


@pytest.fixture
def cmip5_tas():
    return CMIP5_TAS


@pytest.fixture
def cmip6_siconc():
    return CMIP6_SICONC


@pytest.fixture
def cmip6_kerchunk_https_open_json():
    return CMIP6_KERCHUNK_HTTPS_OPEN_JSON


@pytest.fixture
def cmip6_kerchunk_https_open_zst():
    return CMIP6_KERCHUNK_HTTPS_OPEN_ZST


@pytest.fixture
def load_test_data():
    """
    This fixture ensures that the required test data repository
    has been cloned to the cache directory within the home directory.
    """
    branch = "master"
    target = os.path.join(MINI_ESGF_CACHE_DIR, branch)

    if not os.path.isdir(MINI_ESGF_CACHE_DIR):
        os.makedirs(MINI_ESGF_CACHE_DIR)

    if not os.path.isdir(target):
        repo = Repo.clone_from(TEST_DATA_REPO_URL, target)
        repo.git.checkout(branch)

    elif os.environ.get("ROOCS_AUTO_UPDATE_TEST_DATA", "true").lower() != "false":
        repo = Repo(target)
        repo.git.checkout(branch)
        repo.remotes[0].pull()
