import os
import tempfile

from jinja2 import Template

TESTS_HOME = os.path.abspath(os.path.dirname(__file__))
ROOCS_CFG = os.path.join(tempfile.gettempdir(), "roocs.ini")


def write_roocs_cfg():
    cfg_templ = """
    [project:c3s-cmip5]
    base_dir = {{ base_dir }}/mini-esgf-data/test_data/gws/nopw/j04/cp4cds1_vol1/data/c3s-cmip5
    """
    cfg = Template(cfg_templ).render(base_dir=TESTS_HOME)
    with open(ROOCS_CFG, "w") as fp:
        fp.write(cfg)
    # point to roocs cfg in environment
    os.environ["ROOCS_CONFIG"] = ROOCS_CFG
