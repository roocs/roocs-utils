import os
import tempfile
from collections import OrderedDict
from datetime import datetime
from datetime import MAXYEAR
from datetime import MINYEAR
from pathlib import Path

import pandas as pd
import pytest

from roocs_utils import CONFIG
from roocs_utils.catalog_maker.batch import BatchManager
from roocs_utils.catalog_maker.catalog import to_csv
from roocs_utils.catalog_maker.catalog import update_catalog
from roocs_utils.catalog_maker.database import DataBaseHandler
from roocs_utils.catalog_maker.task import TaskManager

here = Path(os.path.dirname(__file__))
MINI_ESGF_CACHE_DIR = Path.home() / ".mini-esgf-data"
MIN_DATETIME = datetime(MINYEAR, 1, 1).isoformat()
MAX_DATETIME = datetime(MAXYEAR, 12, 30).isoformat()


# tests in this test class must be run all in one go to ensure they use the same temporary directory
class TestCatalogMaker:
    @classmethod
    def setup_class(cls):
        cls.tmpdir = tempfile.mkdtemp()
        cls.project = "c3s-cmip6-test"
        cls.catalog_dir = f"{cls.tmpdir}/catalog/"

        CONFIG["project:c3s-cmip6"][
            "base_dir"
        ] = f"{MINI_ESGF_CACHE_DIR}/master/test_data/badc/cmip6/data/CMIP6"
        CONFIG["project:c3s-cmip6-test"]["catalog_dir"] = cls.catalog_dir
        CONFIG["project:c3s-cmip6-test"][
            "csv_dir"
        ] = f"{cls.tmpdir}/catalog/c3s-cmip6-test/"
        CONFIG["project:c3s-cmip6-test"][
            "datasets_file"
        ] = f"{here}/catalog/c3s-cmip6-test/c3s-cmip6-datasets.txt"
        CONFIG["workflow"]["n_per_batch"] = 1

    def test_create_batches(self, load_test_data):
        bm = BatchManager(self.project)
        bm.create_batches()

        batch1 = Path(f"{self.catalog_dir}/{self.project}/batches/batch_0001.txt")
        batch2 = Path(f"{self.catalog_dir}/{self.project}/batches/batch_0002.txt")
        batch3 = Path(f"{self.catalog_dir}/{self.project}/batches/batch_0003.txt")

        batches = [batch1, batch2, batch3]

        for batch in batches:
            # check the batches exist and that there are 3
            assert batch.is_file()

            # check there is one dataset in each one
            file = open(batch, "r")
            nonempty_lines = [line.strip("\n") for line in file if line != "\n"]

            line_count = len(nonempty_lines)
            file.close()

            assert line_count == CONFIG["workflow"]["n_per_batch"]

    @pytest.mark.skipif(
        os.environ.get("ABCUNIT_DB_SETTINGS") is None, reason="database backend not set"
    )
    def test_run(self, load_test_data):
        rh = DataBaseHandler(table_name="c3s_cmip6_test_catalog_results")

        tm = TaskManager(self.project, batches=[1], run_mode="local")
        tm.run_tasks()

        # check the results have been stored
        assert (
            "c3s-cmip6.CMIP.INM.INM-CM5-0.historical.r1i1p1f1.Amon.rlds.gr1.v20190610"
            in rh.get_successful_datasets()
        )

    @pytest.mark.skipif(
        os.environ.get("ABCUNIT_DB_SETTINGS") is None, reason="database backend not set"
    )
    def test_run_time_invariant(self, load_test_data):
        rh = DataBaseHandler(table_name="c3s_cmip6_test_catalog_results")

        tm = TaskManager(self.project, batches=[3], run_mode="local")
        tm.run_tasks()

        # check the results have been stored
        assert (
            "c3s-cmip6.ScenarioMIP.MPI-M.MPI-ESM1-2-LR.ssp370.r1i1p1f1.fx.mrsofc.gn.v20190815"
            in rh.get_successful_datasets()
        )

    @pytest.mark.skipif(
        os.environ.get("ABCUNIT_DB_SETTINGS") is None, reason="database backend not set"
    )
    def test_list(self):
        rh = DataBaseHandler(table_name="c3s_cmip6_test_catalog_results")

        fpaths = rh.get_successful_runs()
        for fpath in fpaths:
            content = rh.get_content(fpath)

            assert (
                fpath
                == f"{MINI_ESGF_CACHE_DIR}/master/test_data/badc/cmip6/data/CMIP6/CMIP/INM/INM-CM5-0/historical/r1i1p1f1/Amon/rlds/gr1/v20190610/rlds_Amon_INM-CM5-0_historical_r1i1p1f1_gr1_185001-194912.nc"
            )
            assert content == dict(
                [
                    (
                        "ds_id",
                        "c3s-cmip6.CMIP.INM.INM-CM5-0.historical.r1i1p1f1.Amon.rlds.gr1.v20190610",
                    ),
                    (
                        "path",
                        "CMIP/INM/INM-CM5-0/historical/r1i1p1f1/Amon/rlds/gr1/v20190610/rlds_Amon_INM-CM5-0_historical_r1i1p1f1_gr1_185001-194912.nc",
                    ),
                    ("size", 251449),
                    ("mip_era", "c3s-cmip6"),
                    ("activity_id", "CMIP"),
                    ("institution_id", "INM"),
                    ("source_id", "INM-CM5-0"),
                    ("experiment_id", "historical"),
                    ("member_id", "r1i1p1f1"),
                    ("table_id", "Amon"),
                    ("variable_id", "rlds"),
                    ("grid_label", "gr1"),
                    ("version", "v20190610"),
                    ("start_time", "1850-01-16T12:00:00"),
                    ("end_time", "1949-12-16T12:00:00"),
                    ("bbox", "0.00, -89.25, 200.00, 60.75"),
                    ("level", " "),
                ]
            )
            break

        assert len(fpaths) == 3

    @pytest.mark.skipif(
        os.environ.get("ABCUNIT_DB_SETTINGS") is None, reason="database backend not set"
    )
    def test_write(self):
        rh = DataBaseHandler(table_name="c3s_cmip6_test_catalog_results")

        # write yaml and csv
        entries = rh.get_all_content()

        path, last_updated = to_csv(entries, self.project)
        update_catalog(self.project, path, last_updated, self.catalog_dir)

        # check it writes csv and yaml files where it should
        yaml = Path(f"{self.catalog_dir}/c3s.yml")
        assert yaml.is_file()

        last_updated = datetime.now().utcnow()
        version_stamp = last_updated.strftime("v%Y%m%d")
        csv = Path(
            f"{self.catalog_dir}/{self.project}/{self.project}_{version_stamp}.csv.gz"
        )
        assert csv.is_file()

        #  open csv and check contents
        df = pd.read_csv(csv)

        assert (
            df["ds_id"][0]
            == "c3s-cmip6.CMIP.INM.INM-CM5-0.historical.r1i1p1f1.Amon.rlds.gr1.v20190610"
        )
        assert df["version"][2] == "v20190815"
        assert df["end_time"][1] == "2014-12-16T12:00:00"
        assert df["start_time"][2] == "undefined"

        # test parsing to min/max datetime
        df = df.replace({"start_time": {"undefined": MIN_DATETIME}})
        df = df.replace({"end_time": {"undefined": MAX_DATETIME}})

        assert df["start_time"][2] == "0001-01-01T00:00:00"

    @pytest.mark.skipif(
        os.environ.get("ABCUNIT_DB_SETTINGS") is None, reason="database backend not set"
    )
    def test_show_errors(self):
        rh = DataBaseHandler(table_name="c3s_cmip6_test_catalog_results")

        assert rh.count_failures() == 0

    @pytest.mark.skipif(
        os.environ.get("ABCUNIT_DB_SETTINGS") is None, reason="database backend not set"
    )
    @classmethod
    def teardown_class(cls):
        rh = DataBaseHandler(table_name="c3s_cmip6_test_catalog_results")
        rh._delete_table()
