from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.exceptions import MissingParameterValue
from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.utils.file_utils import FileMapper


class CollectionParameter(_BaseParameter):
    """
    Class for collection parameter used in operations.

    | A collection can be input as:
    | A string of comma separated values: "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga,cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    | A sequence of strings: e.g. ("cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga", "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga")
    | A sequence of roocs_utils.utils.file_utils.FileMapper objects

    Validates the input and parses the items.

    """

    parse_method = "_parse_sequence"

    def _validate(self):
        if self._result is None:
            raise MissingParameterValue(f"{self.__class__.__name__} must be provided")

        self._parse_items()

    def _parse_items(self):
        for value in self._result:
            if not (isinstance(value, str) or isinstance(value, FileMapper)):
                raise InvalidParameterValue(
                    f"Each id in a collection must be a string or an instance of {FileMapper}"
                )

        return tuple(self._result)

    @property
    def tuple(self):
        """ Returns a tuple of the collection items """
        return self._parse_items()

    def __str__(self):
        string = "Datasets to analyse:"
        for i in self.tuple:
            string += f"\n{i}"
        return string
