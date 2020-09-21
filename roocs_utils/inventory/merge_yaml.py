#!/usr/bin/env python

import yaml
import os
import glob

from roocs_utils.inventory.inventory import CustomDumper

output_dir = "/gws/smf/j04/cp4cds1/c3s_34e/inventory"
current_directory = os.getcwd()
output_base = f"{output_dir}/c3s-cmip5_*.yml"

yaml_files = glob.glob(output_base)


def extend_dict(extend_me, extend_by):
    if isinstance(extend_by, dict):
        for k, v in extend_by.iteritems():
            if k in extend_me:
                extend_dict(extend_me.get(k), v)
            else:
                extend_me[k] = v
    else:
        extend_me += extend_by


# Load the yaml files
for i in range(1, len(yaml_files)-1):
    extend_dict(yaml_files[0], yaml_files[i])


print(yaml.dump(yaml_files[0], default_flow_style=False))

# # create a new file with merged yaml
# with open(f"{output_dir}/c3s-cmip5-merged.yml", 'w') as writer:
#     yaml.dump(yaml_files[0], writer, Dumper=CustomDumper)