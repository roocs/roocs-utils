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

The module ``roocs_utils.catalog_maker`` provides tools for writing data catalogs of the known data holdings in a csv format, described by a YAML file.

For each project in ``roocs_utils/etc/roocs.ini`` there are options to set the file paths for the inputs and outputs of this catalog maker.
A list of datasets to include needs to be provided. The path to this list for each project can be set in ``roocs_utils/etc/roocs.ini``. The datasets in this list must be what you want in the `ds_id` column of the csv file.

The data catalog is created using a database backend to store the results of the scans, from which the csv and YAML files will be created.
For this, a posgresql database is required. Once you have a database, you need to export an environment variable called $ABCUNIT_DB_SETTINGS:

.. code-block::

    $ export ABCUNIT_DB_SETTINGS="dbname=<name> user=<user> host=<host> password=<pwd>"

The table created will be named after the porject you are creating a catalog for in the format <project_name>_catalog_results e.g. c3s_cmip6_catalog_results

Note when using the catalog maker, the dependency abcunit-backend is required. If using a conda environment this must be pip installed manually:

.. code-block::

    $ pip install abcunit-backend

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

This creates a table in the database containing an ordered dictionary of the entry for each file in each dataset if successful, or the error traceback if there is an Exception raised.

Viewing entries and errors
==========================

To view the records:

.. code-block::

    $ python roocs_utils/catalog_maker/cli.py list -p c3s-cmip6

With many entries, this may take a while.


To just get a count of how many files have been scanned:

.. code-block::

    $ python roocs_utils/catalog_maker/cli.py list -p c3s-cmip6 -c


To see any errors:

.. code-block::

    $ python roocs_utils/catalog_maker/cli.py show-errors -p c3s-cmip6


To see just a count of errors:

.. code-block::

    $ python roocs_utils/catalog_maker/cli.py show-errors -p c3s-cmip6 -c


Each count will show how many files and how many datasets have been successful/failed.

The list count will also show the total numbers of datasets/files in the database - including errors.
The error count will show whether there are any datasets that have files which have succeeded and failed i.e. that are partially scanned.


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

Deleting the table of results
=============================

In order to delete all entries in the table of results

.. code-block::

    $ python roocs_utils/catalog_maker/cli.py clean -p c3s-cmip6

Credits
=======

This package was created with ``Cookiecutter`` and the ``audreyr/cookiecutter-pypackage`` project template.


* Cookiecutter: https://github.com/audreyr/cookiecutter
* cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage
