import os
from pathlib import Path
import pytest

from roocs_utils.utils.tutorial import get_file

MINI_ESGF_CACHE_DIR = Path.home() / ".mini-esgf-data"
MINI_ESGF_KWARGS = dict(
    github_url = 'https://github.com/roocs/mini-esgf-data',
    branch = 'master',
    cache_dir = MINI_ESGF_CACHE_DIR
)


def resolve_files(base_dir, kwargs, file_list):
    get_file(
        [os.path.join(base_dir, nc_file) for nc_file in file_list],
        **kwargs
    )
    return os.path.join(kwargs['cache_dir'], kwargs['branch'], base_dir, '*.nc')


@pytest.fixture
def cmip5_tas():
    return resolve_files( 
        'test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas',
        MINI_ESGF_KWARGS,
        ['tas_Amon_HadGEM2-ES_rcp85_r1i1p1_200512-203011.nc',
         'tas_Amon_HadGEM2-ES_rcp85_r1i1p1_209912-212411.nc',
         'tas_Amon_HadGEM2-ES_rcp85_r1i1p1_219912-222411.nc',
         'tas_Amon_HadGEM2-ES_rcp85_r1i1p1_229912-229912.nc',
         'tas_Amon_HadGEM2-ES_rcp85_r1i1p1_203012-205511.nc',
         'tas_Amon_HadGEM2-ES_rcp85_r1i1p1_212412-214911.nc',
         'tas_Amon_HadGEM2-ES_rcp85_r1i1p1_222412-224911.nc',
         'tas_Amon_HadGEM2-ES_rcp85_r1i1p1_205512-208011.nc',
         'tas_Amon_HadGEM2-ES_rcp85_r1i1p1_214912-217411.nc',
         'tas_Amon_HadGEM2-ES_rcp85_r1i1p1_224912-227411.nc',
         'tas_Amon_HadGEM2-ES_rcp85_r1i1p1_208012-209912.nc',
         'tas_Amon_HadGEM2-ES_rcp85_r1i1p1_217412-219911.nc',
         'tas_Amon_HadGEM2-ES_rcp85_r1i1p1_227412-229911.nc']
    )


@pytest.fixture
def cmip5_zostoga():
    return str(get_file(
        'test_data/badc/cmip5/data/cmip5/output1/INM/inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/zostoga_Omon_inmcm4_rcp45_r1i1p1_200601-210012.nc',
        **MINI_ESGF_KWARGS
    ))


@pytest.fixture
def cmip6_siconc():
    return str(get_file(
        'test_data/badc/cmip6/data/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/SImon/siconc/gn/latest/siconc_SImon_CanESM5_historical_r1i1p1f1_gn_185001-201412.nc',
        **MINI_ESGF_KWARGS
    ))


@pytest.fixture
def c3s_cmip5_tas():
    return resolve_files(
        'test_data/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/ICHEC/EC-EARTH/historical/day/atmos/day/r1i1p1/tas/v20131231',
        MINI_ESGF_KWARGS,
        ['tas_day_EC-EARTH_historical_r1i1p1_18500101-18591231.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_19100101-19191231.nc', 
         'tas_day_EC-EARTH_historical_r1i1p1_19700101-19791231.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_18600101-18691231.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_19200101-19291231.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_19800101-19891231.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_18700101-18791231.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_19300101-19391231.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_19900101-19991231.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_18800101-18891231.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_19400101-19491231.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_20000101-20091130.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_18900101-18991231.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_19500101-19591231.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_19000101-19091231.nc',
         'tas_day_EC-EARTH_historical_r1i1p1_19600101-19691231.nc']
    )

