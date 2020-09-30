#!/usr/bin/env python

import oyaml as yaml
import os
import glob

from roocs_utils.inventory.inventory import CustomDumper

output_dir = "/gws/smf/j04/cp4cds1/c3s_34e/inventory"
current_directory = os.getcwd()
output_base = f"{output_dir}/c3s-cmip5_*.yml"

yaml_files = glob.glob(output_base)


def write(new_yaml_data_dict):
    output_path = f"{output_dir}/c3s-cmip5-merged.yml"

    if not os.path.isfile(output_path):

        with open(output_path, "w") as f:
            f.write("---\n")

    sdump = yaml.dump(new_yaml_data_dict, Dumper=CustomDumper)

    with open(output_path, "a") as f:
        f.write(sdump)


for i in range(0, len(yaml_files)):
    with open(yaml_files[i], 'r') as yamlfile1:
        update = yaml.load(yamlfile1, Loader=yaml.SafeLoader)
    write(update)

