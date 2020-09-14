#!/usr/bin/env python

import os
import glob
import yaml
import time
import argparse
import subprocess
from collections import OrderedDict

import xarray as xr

from roocs_utils import CONFIG
from roocs_utils.xarray_utils.xarray_utils import get_coord_type

output_dir = "/gws/smf/j04/cp4cds1/c3s_34e"


def arg_parse():
    parser = argparse.ArgumentParser()

    project_choices = _get_project_list()

    parser.add_argument('-pr', '--project', type=str, choices=project_choices, required=True,
                        help=f'Project, must be one of: {project_choices}')

    return parser.parse_args()


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

    inv_path = f'{output_dir}/{name}.yml'
    with open(inv_path, 'w') as writer: 
        yaml.dump(content, writer, Dumper=CustomDumper)

    print(f'[INFO] Wrote: {inv_path}')


def read_inventory(project):
    inv_path = f'{project}.yml'

    with open(inv_path) as reader:
        data = yaml.load(reader, Loader=yaml.SafeLoader)

    base_dir = data[0]['base_dir']

    for d in data[1:]:
        path = os.path.join(base_dir, d['path'])
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

        ds = xr.open_dataset(fpath, use_cftime=True)
        times = ds[var_id].time.values

        all_times.extend(list(times))
        ds.close()

    return (len(all_times), all_times[0].isoformat() + ' ' + all_times[-1].isoformat())


def get_var_metadata(fpaths, var_id):

    time_length, time_string = get_time_info(fpaths, var_id)

    f1 = fpaths[0]
    print(f'[INFO] Reading {f1}')

    ds = xr.open_dataset(f1, use_cftime=True)
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


def get_coord_info(fpaths):

    ds = xr.open_mfdataset(fpaths, use_cftime=True, combine='by_coords')

    d = OrderedDict()
    
    for coord_id in sorted(ds.coords):

        coord = ds.coords[coord_id]
        type = get_coord_type(coord)

        if type == "time" or type is None:
            continue

        data = coord.values
        mn, mx = data.min(), data.max()
        
        d[f"{type}"] = f"{mn} {mx}"

    return d


def get_size_data(fpaths):

    files = len(fpaths)

    ds = xr.open_mfdataset(fpaths, use_cftime=True, combine='by_coords')

    size = ds.nbytes
    size_gb = size/1E+9

    return size, size_gb, files


def build_dict(dr, proj_dict, base_dir):
    fpaths = glob.glob(f'{dr}/*.nc')

    rel_dir = dr.replace(base_dir, '').strip('/')
    comps = rel_dir.split('/')

    if len(fpaths) < 1:
        d = OrderedDict()
        d['path'] = rel_dir
        d['ds_id'] = rel_dir.replace('/', '.')
        d['Note'] = f"No files available."
        return d

    facet_rule = proj_dict['facet_rule']
    facets = dict([_ for _ in zip(facet_rule, comps)])

    var_id = facets.get('variable') or facets.get('variable_id')

    dims, shape, tm = get_var_metadata(fpaths, var_id)
    size, size_gb, files = get_size_data(fpaths)
    coord_d = get_coord_info(fpaths)

    d = OrderedDict()
    d['path'] = rel_dir
    d['ds_id'] = rel_dir.replace('/', '.')
    d['var_id'] = var_id
    d['array_dims'] = dims
    d['array_shape'] = shape
    d['time'] = tm
    d.update(coord_d)
    d['size'] = size
    d['size_gb'] = size_gb
    d['file_count'] = files
    d['facets'] = facets

    return d


def _get_project_list():
    projects = [_.split(':')[1] for _ in CONFIG.keys() if _.startswith('project:')]
    return projects 


def batch_run(project):
    # queue = "long-serial"
    # wallclock = "168:00"
    
    queue = "short-serial"
    wallclock = "23:59"
    output_base = f"{output_dir}/{project}"
    current_directory = os.getcwd()

    # bsub_cmd = (
    #     f"bsub -q {queue} -W {wallclock} -o "
    #     f"{output_base}.out -e {output_base}.err "
    #     f"{current_directory}/roocs_utils/inventory/run_inventory.py -pr {project}"
    # )
    
    sbatch_cmd = f'sbatch -p {queue} -t {wallclock} -o ' \
                 f'{output_base}.out -e {output_base}.err '  \
                 f'{current_directory}/roocs_utils/inventory/run_inventory.py -pr {project}'

    subprocess.call(sbatch_cmd, shell=True)
    print(f"running {sbatch_cmd}")


if __name__ == '__main__':

    args = arg_parse()
    batch_run(args.project)

