#!/usr/bin/env python

import argparse
import os
import time
import re

from roocs_utils.inventory.inventory import _get_project_list, build_dict, to_yaml
from roocs_utils import CONFIG

_common_c3s_dir = '/group_workspaces/jasmin2/cp4cds1/vol1/data'
VERSION = re.compile('^v\d{8}$')
LIMIT = 1000000000
LIMIT = 1


def arg_parse():
    parser = argparse.ArgumentParser()

    project_choices = _get_project_list()

    parser.add_argument('-pr', '--project', type=str, choices=project_choices, required=True,
                        help=f'Project, must be one of: {project_choices}')

    return parser.parse_args()


def write_inventory(project, d, paths):

    base = d['base_dir']
    header = {'project': project, 'base_dir': base}

    records = [header] + [build_dict(_, d, base) for _ in sorted(paths)]
    to_yaml(project, records)


def _get_start_dir(dr, project):

    if dr.startswith(_common_c3s_dir):
        dr = os.path.join(dr, project)

    return dr


def write_all(project):
    d = CONFIG[f'project:{project}']

    start_dir = _get_start_dir(d['base_dir'], project)
    paths = []

    for item, _1, _2 in os.walk(start_dir):

        if VERSION.match(os.path.basename(item)):
            paths.append(item)

        if len(paths) > LIMIT: break

        if len(paths) > 0 and len(paths) % 100 == 0:
            write_inventory(project, d, paths)
            print(f'[INFO] Written so far: {len(paths)}')

    time.sleep(1)
    write_inventory(project, d, paths)


if __name__ == '__main__':

    args = arg_parse()
    write_all(args.project)
