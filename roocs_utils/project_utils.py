import os

import xarray as xr

from roocs_utils import CONFIG


def map_facet(facet, project):
    # Return mapped value or the same facet name
    proj_mappings = CONFIG[f"project:{project}"]["mappings"]
    return proj_mappings.get(facet, facet)


def get_facet(facet_name, facets, project):
    return facets[map_facet(facet_name, project)]


# move this to config?
project_name_attributes = {
    "cmip5": "project_id",
    "cmip6": "mip_era",
    "cordex": "project_id",
    "c3s-cmip5": "project_id",
    "c3s-cmip6": "NOT DEFINED YET",
    "c3s-cordex": "project_id",
}


def get_project_from_ds(ds):
    for key, value in project_name_attributes.items():
        if ds.attrs.get(value, "").lower() == key:
            project_name = key
            return project_name


def get_base_dirs_dict():
    projects = [_.split(":")[1] for _ in CONFIG.keys() if _.startswith("project:")]
    base_dirs = {
        project: CONFIG[f"project:{project}"]["base_dir"] for project in projects
    }
    return base_dirs


def get_project_name(dset):
    if type(dset) in (xr.core.dataarray.DataArray, xr.core.dataset.Dataset):
        return get_project_from_ds(dset)
    elif dset[0] == "/":
        base_dirs_dict = get_base_dirs_dict()
        for project, base_dir in base_dirs_dict.items():
            if dset.startswith(base_dir):
                return project
    elif dset.count(".") > 6:
        return dset.split(".")[0].lower()
    elif dset.endswith(".nc") or os.path.isfile(dset):
        dset = xr.open_mfdataset(dset, use_cftime=True, combine="by_coords")
        return get_project_from_ds(dset)
    else:
        raise Exception(
            f"The format of {dset} is not known and the project name could not"
            f"be found."
        )


def get_project_base_dir(project):
    try:
        return CONFIG[f"project:{project}"]["base_dir"]
    except KeyError:
        raise Exception("The project supplied is not known.")
