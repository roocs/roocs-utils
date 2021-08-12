import os
import tempfile
from pathlib import Path

from jinja2 import Template

MINI_ESGF_CACHE_DIR = Path.home() / ".mini-esgf-data"
ROOCS_CFG = os.path.join(tempfile.gettempdir(), "roocs.ini")


def write_roocs_cfg():
    cfg_templ = """
    [project:c3s-cmip5]
    base_dir = {{ base_dir }}/master/test_data/gws/nopw/j04/cp4cds1_vol1/data/c3s-cmip5

    [project:proj_test]
    base_dir = /projects/test/proj
    fixed_path_modifiers =
        variable:rain sun cloud
    fixed_path_mappings =
        proj_test.my.first.test:first/test/something.nc
        proj_test.my.second.test:second/test/data_*.txt
        proj_test.another.{variable}.test:good/test/{variable}.nc
    """
    cfg = Template(cfg_templ).render(base_dir=MINI_ESGF_CACHE_DIR)
    with open(ROOCS_CFG, "w") as fp:
        fp.write(cfg)
    # point to roocs cfg in environment
    os.environ["ROOCS_CONFIG"] = ROOCS_CFG
