#!/usr/bin/env python

import os
import re
import glob
import yaml
import time
from collections import OrderedDict

import xarray as xr

from roocs_utils import CONFIG

_common_c3s_dir = '/group_workspaces/jasmin2/cp4cds1/vol1/data'

VERSION = re.compile('^v\d+$')
LIMIT = 1000000000
LIMIT = 1


class CustomDumper(yaml.SafeDumper):
    # Inserts blank lines between top-level objects: inspired by https://stackoverflow.com/a/44284819/3786245"
    # Preserve the mapping key order. See https://stackoverflow.com/a/52621703/1497385"
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()

    def represent_dict_preserve_order(self, data):
        return self.represent_dict(data.items())    


CustomDumper.add_representer(OrderedDict, CustomDumper.represent_dict_preserve_order)


def to_yaml(name, content):

    inv_path = f'{name}.yml'
    with open(inv_path, 'w') as writer: 
        yaml.dump(content, writer, Dumper=CustomDumper)

    print(f'[INFO] Wrote: {inv_path}')


def read_inventory(project):
    inv_path = f'{project}.yml'

    with open(inv_path) as reader:
        data = yaml.load(reader, Loader=yaml.SafeLoader)

    base_dir = data[0]['base_dir']

    for d in data[1:]:
        path = os.path.join(basedir, d['path'])
        d['path'] = path

    return {'header': data[0], 'records': data[1:]}


def test_all():
    data = [
        {'base_dir': 'bsfdsd', 'other': 'sdfsf'},
        {'dsid': 'sdfsd.fs.fs.fs.fsd.', 'dims': 'lat, lon'}
    ]
    to_yaml('x', data)


def get_time_info(fpaths, var_id):

    all_times = []

    for fpath in sorted(fpaths):

        ds = xr.open_dataset(fpath)
        times = ds[var_id].time.values

        all_times.extend(list(times))
        ds.close()

    return (len(all_times), all_times[0].isoformat() + ' ' + all_times[-1].isoformat())


def get_var_metadata(dr, var_id):

    fpaths = glob.glob(f'{dr}/*.nc')
    time_length, time_string = get_time_info(fpaths, var_id)

    f1 = fpaths[0]
    print(f'[INFO] Reading {f1}')

    ds = xr.open_dataset(f1)
    dims = ds[var_id].dims

    shape_annotated = []

    for i in range(len(dims)):
        dim = dims[i]
        length = ds[var_id].shape[i]

        if dim.startswith('time'):
            item = str(time_length) 
        else:
            item = str(length)
    
        shape_annotated.append(item)    

    dims = ' '.join(list(dims))
    shape = ' '.join(list(shape_annotated))
    
    ds.close()

    return dims, shape, time_string


def build_dict(dr, proj_dict, base_dir):
    rel_dir = dr.replace(base_dir, '').strip('/')
    comps = rel_dir.split('/')

    facet_rule = proj_dict['facet_rule']
    facets = dict([_ for _ in zip(facet_rule, comps)])
    var_id = facets['variable']

    dims, shape, tm = get_var_metadata(dr, var_id)

    d = OrderedDict()
    d['path'] = rel_dir
    d['dsid'] = rel_dir.replace('/', '.')
    d['var_id'] = var_id
    d['array_dims'] = dims
    d['array_shape'] = shape
    d['time'] = tm
    d['facets'] = facets

    return d


def write_inventory(project, d, paths):

    base = d['base_dir']
    header = {'project': project, 'base_dir': base}

    records = [header] + [build_dict(_, d, base) for _ in sorted(paths)]
    to_yaml(project, records)


def _get_project_list():
    projects = [_.split(':')[1] for _ in CONFIG.keys() if _.startswith('project:')]
    return projects 


def _get_start_dir(dr, project):

    if dr.startswith(_common_c3s_dir):
        dr = os.path.join(dr, project)

    return dr 


def write_all():

    for project in _get_project_list(): 

        if project != 'c3s-cmip5': continue
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

    #test_all()
    write_all()
    #inv = read_inventory('c3s-cmip5')
