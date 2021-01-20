.. highlight:: shell

=============
Installation
=============

Stable release
--------------

To install roocs-utils, run this command in your terminal:

.. code-block:: console

    $ pip install roocs-utils

This is the preferred method to install roocs-utils, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Install from GitHub
-------------------

roocs-utils can be downloaded from the `Github repo`_.

.. code-block:: console

    $ git clone git://github.com/roocs/roocs-utils
    $ cd roocs-utils


Create Conda environment named `roocs_utils`:

.. code-block:: console

   $ conda env create -f environment.yml
   $ source activate roocs_utils


Install roocs-utils in development mode:

.. code-block:: console

    $ pip install -r requirements.txt
    $ pip install -r requirements_dev.txt
    $ pip install -e .

Run tests:

.. code-block:: console

    $ python -m pytest tests/

.. _Github repo: https://github.com/roocs/roocs-utils
