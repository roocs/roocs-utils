from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.parameter.base_parameter import _BaseParameter


class AreaParameter(_BaseParameter):
    """
    Class for area parameter used in subsetting operation.

    | Area can be input as:
    | A string of comma separated values: "0.,49.,10.,65"
    | A sequence of strings: ("0", "-10", "120", "40")
    | A sequence of numbers: [0, 49.5, 10, 65]

    An area must have 4 values.

    Validates the area input and parses the values into numbers.

    """

    parse_method = "_parse_sequence"

    def _validate(self):

        if self._result is not None and len(self._result) != 4:
            raise InvalidParameterValue(
                f"{self.__class__.__name__} should be of length 4 but is of length "
                f"{len(self._result)}"
            )
        self._parse_values()

    def _parse_values(self):
        if self._result is None:
            return self._result

        area = []
        for value in self._result:
            if isinstance(value, str):
                if not value.replace(".", "", 1).strip("-").isdigit():
                    raise InvalidParameterValue("Area values must be a number")
            else:
                if not (isinstance(value, float) or isinstance(value, int)):
                    raise InvalidParameterValue("Area values must be a number")

            area.append(float(value))

        return tuple(area)

    @property
    def tuple(self):
        """ Returns a tuple of the area values """
        return self._parse_values()

    def asdict(self):
        """ Returns a dictionary of the area values """
        if self.tuple is not None:
            return {
                "lon_bnds": (self.tuple[0], self.tuple[2]),
                "lat_bnds": (self.tuple[1], self.tuple[3]),
            }

    def __str__(self):
        return f"Area to subset over:" f"\n {self.tuple}"
