roocs-utils
===========

.. image:: https://img.shields.io/pypi/v/roocs_utils.svg
   :target: https://pypi.python.org/pypi/roocs_utils
   :alt: Pypi



.. image:: https://img.shields.io/travis/roocs/roocs-utils.svg
   :target: https://travis-ci.com/roocs/roocs-utils
   :alt: Travis



.. image:: https://readthedocs.org/projects/roocs-utils/badge/?version=latest
   :target: https://roocs-utils.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation


A package containing common components for the roocs project


* Free software: BSD - see LICENSE file in top-level package directory
* Documentation: https://roocs-utils.readthedocs.io.

Features
--------


*

  #. Data Inventories

1. Data Inventories
^^^^^^^^^^^^^^^^^^^

The module ``roocs_utils.inventory`` provides tools for writing inventories of the known
data holdings in a YAML format.

For each project in ``roocs_utils/etc/roocs.ini`` there are options to set the file paths for the inputs and outputs of this inventory maker.
A list of datasets to include in the inventory needs to be provided. The path to this list for each project can be set in ``roocs_utils/etc/roocs.ini``

Once the list of datasets is collated a number of batches must be created:

.. code-block:: shell

    $ python roocs_utils/inventory/cli.py create-batches -p c3s-cmip6 
    
The option ``-p`` is required to specify the project.

Once the batches are created, the inventory maker can be run - either locally or on lotus. 

Each batch can be run idependently, e.g. running batch 1 locally:

.. code-block:: shell

    $ python roocs_utils/inventory/cli.py run -p c3s-cmip6 -b 1 -r local 
    
or running all batches on lotus:

.. code-block:: shell

    $ python roocs_utils/inventory/cli.py run -p c3s-cmip6 -r lotus
    
The settings for how many datasets to be included in a batch and the maximum duration of each job on lotus can also be changed in ``roocs_utils/etc/roocs.ini``.

This creates a pickle file ...

.. code-block:: shell

   $ python roocs_utils/inventory/inventory.py -pr c3s-cmip5
   [INFO] Reading /group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/MOHC/HadGEM2-ES/rcp45/mon/atmos/Amon/r1i1p1/tas/v20111                                                                  128/tas_Amon_HadGEM2-ES_rcp45_r1i1p1_212412-214911.nc
   [INFO] Reading /group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/MOHC/HadGEM2-ES/rcp45/mon/atmos/Amon/r1i1p1/ts/v201111                                                                  28/ts_Amon_HadGEM2-ES_rcp45_r1i1p1_209912-212411.nc
   [INFO] Wrote: c3s-cmip5_MOHC_HadGEM2-ES.yml

One file is created for each model/institute pairing. These can be merged to one file
using ``roocs_utils/inventory/merge_yaml.py``

Writes:

.. code-block:: shell

   - base_dir: /group_workspaces/jasmin2/cp4cds1/vol1/data/
     project: c3s-cmip5

   - path: c3s-cmip5/output1/MOHC/HadGEM2-ES/rcp45/mon/atmos/Amon/r1i1p1/tas/v20111128
     dsid: c3s-cmip5.output1.MOHC.HadGEM2-ES.rcp45.mon.atmos.Amon.r1i1p1.tas.v20111128
     var_id: tas
     array_dims: time lat lon
     array_shape: 3529 145 192
     time: 2005-12-16T00:00:00 2299-12-16T00:00:00
     facets:
       activity: c3s-cmip5
       ensemble_member: r1i1p1
       experiment: rcp45
       frequency: mon
       institute: MOHC
       mip_table: Amon
       model: HadGEM2-ES
       product: output1
       realm: atmos
       variable: tas
       version: v20111128

Credits
=======

This package was created with ``Cookiecutter`` and the ``audreyr/cookiecutter-pypackage`` project template.


* Cookiecutter: https://github.com/audreyr/cookiecutter
* cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage
