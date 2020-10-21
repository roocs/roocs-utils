import numbers

from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.parameter.base_parameter import _BaseParameter


class LevelParameter(_BaseParameter):
    """
    Class for level parameter used in subsetting operation.

    | Level can be input as:
    | A string of slash separated values: "1000/2000"
    | A sequence of strings: e.g. ("1000.50", "2000.60")
    | A sequence of numbers: e.g. (1000.50, 2000.60)

    A level input must be 2 values.

    If using a string input a trailing slash indicates you want to use the lowest/highest
    level of the dataset. e.g. "/2000" will subset from the lowest level in the dataset
    to 2000.

    Validates the level input and parses the values into numbers.

    """

    parse_method = "_parse_range"

    def _validate(self):
        self._parse_levels()

    def _parse_levels(self):
        result = [None, None]

        for count, value in enumerate(self._result):
            if value is None:
                continue

            if isinstance(value, str):
                try:
                    value = float(value)
                except Exception:
                    raise InvalidParameterValue("Level values must be a number")

            if not isinstance(value, numbers.Number):
                raise InvalidParameterValue("Level values must be a number")

            result[count] = value

        return tuple(result)

    @property
    def tuple(self):
        """ Returns a tuple of the level values """
        return self._parse_levels()

    def asdict(self):
        """ Returns a dictionary of the level values """
        return {"first_level": self.tuple[0], "last_level": self.tuple[1]}

    def __str__(self):
        return (
            f"Level range to subset over"
            f"\n first_level: {self.tuple[0]}"
            f"\n last_level: {self.tuple[1]}"
        )
