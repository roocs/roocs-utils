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

  #. Intake Catalog

1. Data Catalog
^^^^^^^^^^^^^^^

The module ``roocs_utils.inventory`` provides tools for writing data catalogs of the known
data holdings in a csv format, described by a YAML file.

For each project in ``roocs_utils/etc/roocs.ini`` there are options to set the file paths for the inputs and outputs of this catalog maker.
A list of datasets to include needs to be provided. The path to this list for each project can be set in ``roocs_utils/etc/roocs.ini``


Creating batches
================

Once the list of datasets is collated a number of batches must be created:

.. code-block::

    $ python roocs_utils/catalog_maker/cli.py create-batches -p c3s-cmip6

The option ``-p`` is required to specify the project.

Creating catalog entries
========================

Once the batches are created, the catalog maker can be run - either locally or on lotus. The settings for how many datasets to be included in a batch and the maximum duration of each job on lotus can also be changed in ``roocs_utils/etc/roocs.ini``.

Each batch can be run idependently, e.g. running batch 1 locally:

.. code-block::

    $ python roocs_utils/catalog_maker/cli.py run -p c3s-cmip6 -b 1 -r local

or running all batches on lotus:

.. code-block::

    $ python roocs_utils/catalog_maker/cli.py run -p c3s-cmip6 -r lotus

This creates a pickle file containing an ordered dictionary of the entry for each file in each dataset. It also creates a pickle file for any errors.

Viewing entries and errors
==========================

To view the records:

.. code-block::

    $ python roocs_utils/catalog_maker/cli.py list -p c3s-cmip6

and to see any errors:

.. code-block::

    $ python roocs_utils/catalog_maker/cli.py show-errors -p c3s-cmip6

To just get a count of how many files have been scanned:

.. code-block::

    $ python roocs_utils/catalog_maker/cli.py list -p c3s-cmip6 -c

Writing to CSV
==============

The final command is to write the entries to a csv file.

.. code-block::

    $ python roocs_utils/catalog_maker/cli.py write -p c3s-cmip6

The csv file will be generated in the ``csv_dir`` specified in ``roocs_utils/etc/roocs.ini`` and will have the name "{project}_{version_stamp}.csv".
e.g. c3s-cmip6_v20210414.csv

A yaml file will be created the ``catalog_dir`` specified in ``roocs_utils/etc/roocs.ini``.
It will have the name ``c3s.yml`` and will contain the below for each project scanned and which is using the same ``catalog_dir``:

.. code-block::

    sources:
      c3s-cmip6:
        args:
          urlpath:
        cache:
        - argkey: urlpath
          type: file
        description: c3s-cmip6 datasets
        driver: intake.source.csv.CSVSource
        metadata:
          last_updated:

``urlpath`` and ``last_updated`` for a project will be updated very time the csv file is written for the project.

Credits
=======

This package was created with ``Cookiecutter`` and the ``audreyr/cookiecutter-pypackage`` project template.


* Cookiecutter: https://github.com/audreyr/cookiecutter
* cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage
