import os

import xarray as xr

from roocs_utils import CONFIG


class MapDataset:  # better name??
    def __init__(self, dset, project=None):
        """ can only be used with ds ids or data paths"""
        self._project = project
        self.dset = dset

        self._base_dir = None
        self._ds_id = None
        self._data_path = None

        self._parse()

    def get_base_dirs_dict(self):

        projects = [_.split(":")[1] for _ in CONFIG.keys() if _.startswith("project:")]
        base_dirs = {
            project: CONFIG[f"project:{project}"]["base_dir"] for project in projects
        }
        return base_dirs

    def deduce_project(self):

        if isinstance(self.dset, str):
            if self.dset.count(".") > 6:
                return self.dset.split(".")[0].lower()

            elif self.dset.startswith("/"):
                # by default this returns c3s-cmip6 not cmip6 (as they have the same base_dir)
                base_dirs_dict = self.get_base_dirs_dict()
                for project, base_dir in base_dirs_dict.items():
                    if (
                        self.dset.startswith(base_dir)
                        and CONFIG[f"project:{project}"].get(
                            "is_default_for_path", True
                        )
                        is True
                    ):
                        return project

            # this will not return c3s project names
            elif self.dset.endswith(".nc") or os.path.isfile(self.dset):
                dset = xr.open_mfdataset(
                    self.dset, use_cftime=True, combine="by_coords"
                )
                return get_project_from_ds(dset)

        else:
            raise Exception(
                f"The format of {self.dset} is not known and the project name could not"
                f"be found."
            )

    def _parse(self):

        if not self._project:
            self._project = self.deduce_project()

        if not self._project:
            return

        self._base_dir = get_project_base_dir(self._project)

        if self.dset.count(".") > 6:
            self._ds_id = self.dset
            self._data_path = os.path.join(
                self._base_dir, "/".join(self.dset.split(".")[1:])
            )
        # need to include project here
        elif self.dset.startswith("/"):
            self._data_path = self.dset
            # think i need to include a project here
            self._ds_id = ".".join(
                self.dset.replace(self._base_dir, "").strip("/").split("/")
            )

        # set facets/files?

    @property
    def raw(self):
        return self.dset

    @property
    def data_path(self):
        return self._data_path

    @property
    def ds_id(self):
        return self._ds_id

    @property
    def base_dir(self):
        return self._base_dir

    # @property
    # def facets(self):
    #
    # @property
    # def files(self):


# You could imagine some utility functions that wrap the Dataset class.
def derive_dset(dset):
    return MapDataset(dset)


def open_xr_dataset(dset):
    pass


def datapath_to_dsid(datapath):
    return MapDataset(datapath).ds_id


def dsid_to_datapath(dsid):
    return MapDataset(dsid).ds_id


def get_project_from_ds(ds):

    for project in [_.split(":")[1] for _ in CONFIG.keys() if _.startswith("project:")]:
        key = map_facet("project", project)
        if ds.attrs.get(key, "").lower() == project:
            return project


def get_project_name(dset):

    if type(dset) in (xr.core.dataarray.DataArray, xr.core.dataset.Dataset):
        return get_project_from_ds(dset)  # will not return c3s dataset

    else:
        ds = MapDataset(dset)
        return ds.deduce_project()


def map_facet(facet, project):
    # Return mapped value or the same facet name
    proj_mappings = CONFIG[f"project:{project}"]["mappings"]
    return proj_mappings.get(facet, facet)


def get_facet(facet_name, facets, project):
    return facets[map_facet(facet_name, project)]


def get_project_base_dir(project):
    try:
        return CONFIG[f"project:{project}"]["base_dir"]
    except KeyError:
        raise Exception("The project supplied is not known.")
