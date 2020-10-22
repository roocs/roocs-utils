Version History
===============
v0.1.4 (2020-10-22)
-------------------

Fixing pip install


Bug Fixes
^^^^^^^^^


* Importing and using roocs-utils when pip installing now works


v0.1.3 (2020-10-21)
-------------------

Fixing formatting of doc strings


New Features
^^^^^^^^^^^^


* Added a notebook to show examples



Other Changes
^^^^^^^^^^^^^


* Updated formatting of doc strings


v0.1.2 (2020-10-15)
-------------------

Updating the documentation and improving the changelog.



Other Changes
^^^^^^^^^^^^^


* Updated doc strings to improve documentation.
* Updated documentation.

v0.1.1 (2020-10-12)
-------------------

Fixing mostly existing functionality to work more efficiently with the other packages in roocs.



Breaking Changes
^^^^^^^^^^^^^^^^


* ``environment.yml`` has been updated to bring it in line with requirements.txt.
* ``level`` coordinates would previously have been identified as ``None``. They are now identified as ``level``.

New Features
^^^^^^^^^^^^


* ``parameterise`` function added in ``roocs_utils.parameter`` to use in all roocs packages.
* ``ROOCS_CONFIG`` environment variable can be used to override default config in ``etc/roocs.ini``.
  To use a local config file set ``ROOCS_CONFIG`` as the file path to this file. Several file paths can be provided
  separated by a ``:``
* Inventory functionality added - this can be used to create an inventory of datasets. See ``README`` for more info.
* ``project_utils`` added with the following functions to get the project name of a dataset and the base directory for
  that project.
* ``utils.common`` and ``utils.time_utils`` added.
* ``is_level`` implemented in ``xarray_utils`` to identify whether a coordinate is a level or not.

Bug Fixes
^^^^^^^^^


* ``xarray_utils.xarray_utils.get_main_variable`` updated to exclude common coordinates from the search for the
  main variable. This fixes a bug where coordinates such as ``lon_bounds`` would be returned as the main variable.

Other Changes
^^^^^^^^^^^^^


* ``README`` update to explain inventory functionality.
* ``Black`` and ``flake8`` formatting applied.
* Fixed import warning with ``collections.abc``.

v0.1.0 (2020-07-30)
-------------------


* First release.
