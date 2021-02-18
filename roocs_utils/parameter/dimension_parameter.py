from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.xarray_utils.xarray_utils import known_coord_types


class DimensionParameter(_BaseParameter):
    """
    Class for dimensions parameter used in averaging operation.

    | Area can be input as:
    | A string of comma separated values: "time,latitude,longitude"
    | A sequence of strings: ("time", "longitude")

    Dimensions can be None or any number of options from time, latitude, longitude and level provided these
    exist in the dataset being operated on.

    Validates the dims input and parses the values into a sequence of strings.

    """

    parse_method = "_parse_sequence"

    def _validate(self):

        self._parse_dims()

    def _parse_dims(self):
        if self._result is None:
            return self._result

        for value in self._result:
            if not (isinstance(value, str)):
                raise InvalidParameterValue(f"Each dimension must be a string.")
            if value not in known_coord_types:
                raise InvalidParameterValue(
                    f"Dimensions for averaging must be one of {known_coord_types}"
                )

        return tuple(self._result)

    @property
    def tuple(self):
        """ Returns a tuple of the dimensions """
        return self._parse_dims()

    def asdict(self):
        """ Returns a dictionary of the dimensions """
        if self.tuple is not None:
            return {"dims": self.tuple}

    def __str__(self):
        return f"Dimensions to average over:" f"\n {self.tuple}"
