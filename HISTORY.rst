Version History
===============

v0.3.0 (2021-03-30)
-------------------
New Features
^^^^^^^^^^^^
* Added ``AnyCalendarDateTime`` and ``str_to_AnyCalendarDateTime`` to ``utils.time_utils`` to aid in handling date strings that may not exist in all calendar types.
* Inventory maker will check latitude and longitude of the dataset it is scanning are within acceptable bounds and raise an exception if they are not.


v0.2.1 (2021-02-19)
-------------------
Bug Fixes
^^^^^^^^^
* clean up imports ... remove pandas dependency.

v0.2.0 (2021-02-18)
-------------------

Breaking Changes
^^^^^^^^^^^^^^^^
* cf_xarray>=0.3.1 now required due to differing level identification of coordinates between versions.
* oyaml>=0.9 - new dependency for inventory
* Interface to inventory maker changed. Detailed instructions for use added in README.
* Adjusted file name template. Underscore removed before ``__derive__time_range``
* New dev dependency: GitPython==3.1.12

New Features
^^^^^^^^^^^^
* Added ``use_inventory`` option to ``roocs.ini`` config and allow data to be used without checking an inventory.
* ``DatasetMapper`` class and wrapper functions added to ``roocs_utils.project_utils`` and ``roocs_utils.xarray_utils.xarray_utils`` to resolve all paths and dataset ids in the same way.
* ``FileMapper`` added in ``roocs_utils.utils.file_utils`` to resolve resolve multiple files with the same directory to their directory path.
* Fixed path mapping support added in ``DatasetMapper``
* Added ``DimensionParameter`` to be used with the average operation.

Other Changes
^^^^^^^^^^^^^
* Removed submodule for test data. Test data is now cloned from git using GitPython and cached
* ``CollectionParamter`` accepts an instance of ``FileMapper`` or a sequence of ``FileMapper`` objects
* Adjusted file name template to include an ``extra`` option before the file extension.
* Swapped from travis CI to GitHub actions

v0.1.5 (2020-11-23)
-------------------

Breaking Changes
^^^^^^^^^^^^^^^^

* Replaced use of ``cfunits`` by ``cf_xarray`` and ``cftime`` (new dependency) in ``roocs_utils.xarray_utils``.


v0.1.4 (2020-10-22)
-------------------

Fixing pip install


Bug Fixes
^^^^^^^^^


* Importing and using roocs-utils when pip installing now works


v0.1.3 (2020-10-21)
-------------------

Fixing formatting of doc strings and imports


Breaking Changes
^^^^^^^^^^^^^^^^


* Use of ``roocs_utils.parameter.parameterise.parameterise``:
import should now be ``from roocs_utils.parameter import parameterise``
and usage should be, for example ``parameters = parameterise(collection=ds, time=time, area=area, level=level)``


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
