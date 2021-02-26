roocs-utils
===========

.. image:: https://img.shields.io/pypi/v/roocs_utils.svg
   :target: https://pypi.python.org/pypi/roocs_utils
   :alt: Pypi

.. image:: https://github.com/roocs/roocs-utils/workflows/build/badge.svg
    :target: https://github.com/roocs/roocs-utils/actions
    :alt: Build Status

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


Creating batches
================

Once the list of datasets is collated a number of batches must be created:

.. code-block::

    $ python roocs_utils/inventory/cli.py create-batches -p c3s-cmip6

The option ``-p`` is required to specify the project.

Creating inventory records
==========================

Once the batches are created, the inventory maker can be run - either locally or on lotus. The settings for how many datasets to be included in a batch and the maximum duration of each job on lotus can also be changed in ``roocs_utils/etc/roocs.ini``.

Each batch can be run idependently, e.g. running batch 1 locally:

.. code-block::

    $ python roocs_utils/inventory/cli.py run -p c3s-cmip6 -b 1 -r local

or running all batches on lotus:

.. code-block::

    $ python roocs_utils/inventory/cli.py run -p c3s-cmip6 -r lotus

This creates a pickle file containing an ordered dictionary of the inventory for each dataset. It also creates a pickle file for any errors.

Viewing records and errors
==========================

To view the records:

.. code-block::

    $ python roocs_utils/inventory/cli.py list -p c3s-cmip6

and to see any errors:

.. code-block::

    $ python roocs_utils/inventory/cli.py show-errors -p c3s-cmip6

To just get a count of how many datasets have been scanned:

.. code-block::

    $ python roocs_utils/inventory/cli.py list -p c3s-cmip6 -c

Writing the inventory
=====================

The final command is to write the inventory to a yaml file. There are 2 options for this.

1.

.. code-block::

    $ python roocs_utils/inventory/cli.py write -p c3s-cmip6 -v files

writes the inventory file ``c3s-cmip6-inventory-files.yml`` and includes the file names for each dataset:


.. code-block::

    - path: ScenarioMIP/CCCma/CanESM5/ssp370/r1i1p1f1/Amon/rsutcs/gn/v20190429
      ds_id: c3s-cmip6.ScenarioMIP.CCCma.CanESM5.ssp370.r1i1p1f1.Amon.rsutcs.gn.v20190429
      var_id: rsutcs
      array_dims: time lat lon
      array_shape: 1032 64 128
      time: 2015-01-16T12:00:00 2100-12-16T12:00:00
      latitude: -87.86 87.86
      longitude: 0.00 357.19
      size: 33845952
      size_gb: 0.03
      file_count: 1
      facets:
        mip_era: c3s-cmip6
        activity_id: ScenarioMIP
        institution_id: CCCma
        source_id: CanESM5
        experiment_id: ssp370
        member_id: r1i1p1f1
        table_id: Amon
        variable_id: rsutcs
        grid_label: gn
        version: v20190429
      files:
      - rsutcs_Amon_CanESM5_ssp370_r1i1p1f1_gn_201501-210012.nc

2.

.. code-block::

    $ python roocs_utils/inventory/cli.py write -p c3s-cmip6 -v c3s

writes the inventory file ``c3s-cmip6-inventory.yml`` and does not include file names:


.. code-block::

    - path: ScenarioMIP/CCCma/CanESM5/ssp370/r1i1p1f1/Amon/rsutcs/gn/v20190429
      ds_id: c3s-cmip6.ScenarioMIP.CCCma.CanESM5.ssp370.r1i1p1f1.Amon.rsutcs.gn.v20190429
      var_id: rsutcs
      array_dims: time lat lon
      array_shape: 1032 64 128
      time: 2015-01-16T12:00:00 2100-12-16T12:00:00
      latitude: -87.86 87.86
      longitude: 0.00 357.19
      size: 33845952
      size_gb: 0.03
      file_count: 1
      facets:
        mip_era: c3s-cmip6
        activity_id: ScenarioMIP
        institution_id: CCCma
        source_id: CanESM5
        experiment_id: ssp370
        member_id: r1i1p1f1
        table_id: Amon
        variable_id: rsutcs
        grid_label: gn
        version: v20190429

Files is the default and will happen when no version is provided.

Credits
=======

This package was created with ``Cookiecutter`` and the ``audreyr/cookiecutter-pypackage`` project template.


* Cookiecutter: https://github.com/audreyr/cookiecutter
* cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage
