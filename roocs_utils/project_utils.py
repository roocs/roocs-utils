from roocs_utils.config import _CONFIG as CONFIG


# from dachar
def map_facet(facet, project):
    # Return mapped value or the same facet name
    proj_mappings = CONFIG[f'project:{project}']['mappings']
    return proj_mappings.get(facet, facet)


def get_facet(facet_name, facets, project):
    return facets[map_facet(facet_name, project)]


def get_project_base_dir(project):
    return CONFIG[f'project:{project}']['base_dir']
