#!/usr/bin/env python

import argparse
import os
import time
import re

from roocs_utils.inventory.inventory import _get_project_list, build_dict, to_yaml
from roocs_utils import CONFIG


VERSION = re.compile('^v\d{8}$')
LIMIT = 1000000000
LIMIT = 1


def arg_parse():
    parser = argparse.ArgumentParser()

    project_choices = _get_project_list()

    parser.add_argument('-pr', '--project', type=str, choices=project_choices, required=True,
                        help=f'Project, must be one of: {project_choices}')
    parser.add_argument('-m', '--model', type=str, required=True)

    return parser.parse_args()


def write_inventory(project, model_inst, d, paths):

    base = d['base_dir']
    header = {'project': project, 'base_dir': base}

    records = [header] + [build_dict(_, d, base) for _ in sorted(paths)]
    name = f"{project}_{model_inst}"

    to_yaml(name, records)


def write_all(project, model_path):
    d = CONFIG[f'project:{project}']

    start_dir = model_path
    model_inst = '_'.join(model_path.split('/')[-3:-1])

    paths = []

    for item, _1, _2 in os.walk(start_dir):

        if VERSION.match(os.path.basename(item)):
            paths.append(item)

        if len(paths) > LIMIT: break

        if len(paths) > 0 and len(paths) % 100 == 0:
            write_inventory(project, model_inst, d, paths)
            print(f'[INFO] Written so far: {len(paths)}')

    time.sleep(1)
    write_inventory(project, model_inst, d, paths)


if __name__ == '__main__':

    args = arg_parse()
    write_all(args.project, args.model)
