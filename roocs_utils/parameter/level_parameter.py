import numbers

from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.parameter.base_parameter import _BaseIntervalOrSeriesParameter
from roocs_utils.parameter.param_utils import (parse_range, parse_sequence,
                            to_float, interval, series)


class LevelParameter(_BaseIntervalOrSeriesParameter):
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

    def _parse_as_interval(self):
        value = tuple([to_float(i) for i in self.input.value])

        if set(value) == {None}:
            value = None

        return value

    def _parse_as_series(self):
        return [to_float(i) for i in self.input.value if i is not None]

    def asdict(self):
        """Returns a dictionary of the level values"""
        value = self._value_as_tuple()
        return {"first_level": value[0], "last_level": value[1]}

    def __str__(self):
        value = self._value_as_tuple()
        return (
            f"Level range to subset over"
            f"\n first_level: {value[0]}"
            f"\n last_level: {value[1]}"
        )
