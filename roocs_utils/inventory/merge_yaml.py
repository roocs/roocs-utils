#!/usr/bin/env python
import glob
import os

import oyaml as yaml

from roocs_utils.inventory.inventory import CustomDumper

output_dir = "/gws/smf/j04/cp4cds1/c3s_34e/inventory"
current_directory = os.getcwd()
output_base = f"{output_dir}/c3s-cordex_*.yml"

yaml_files = glob.glob(output_base)


def write(new_yaml_data_dict):
    if not os.path.isfile(yaml_files[0]):

        with open(yaml_files[0], "a") as f:
            f.write("---\n")

    sdump = yaml.dump(new_yaml_data_dict, Dumper=CustomDumper)

    with open(f"{output_dir}/c3s-cordex-merged.yml", "a") as f:
        f.write(sdump)


for i in range(1, len(yaml_files) - 1):
    with open(yaml_files[i], "r") as yamlfile1:
        cmip5_update = yaml.load(yamlfile1, Loader=yaml.SafeLoader)
    write(cmip5_update)
