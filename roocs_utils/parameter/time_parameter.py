import datetime

from dateutil import parser as date_parser

from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.parameter.base_parameter import _BaseParameter


class TimeParameter(_BaseParameter):
    """
    Class for time parameter used in subsetting operation.

    | Time can be input as:
    | A string of slash separated values: "2085-01-01T12:00:00Z/2120-12-30T12:00:00Z"
    | A sequence of strings: e.g. ("2085-01-01T12:00:00Z", "2120-12-30T12:00:00Z")

    A time input must be 2 values.

    If using a string input a trailing slash indicates you want to use the earliest/
    latest time of the dataset. e.g. "2085-01-01T12:00:00Z/" will subset from 01/01/2085 to the final time in
    the dataset.

    Validates the times input and parses the values into isoformat.

    """

    parse_method = "_parse_range"

    def _validate(self):
        try:
            self._parse_times()

        except (date_parser._parser.ParserError, TypeError):
            raise InvalidParameterValue("Unable to parse the time values entered")

    def _parse_times(self):
        # should this default to the start and end time of the data?
        start, end = self._result

        if start is not None:
            start = date_parser.parse(
                start, default=datetime.datetime(datetime.MINYEAR, 1, 1)
            ).isoformat()
        if end is not None:
            end = date_parser.parse(
                end, default=datetime.datetime(datetime.MAXYEAR, 12, 30)
            ).isoformat()

        return start, end

    @property
    def tuple(self):
        """ Returns a tuple of the time values """
        if self._parse_times() is not (None, None):
            return self._parse_times()

    def asdict(self):
        """Returns a dictionary of the time values"""
        if self.tuple is not None:
            return {"start_time": self.tuple[0], "end_time": self.tuple[1]}

    def __str__(self):
        return (
            f"Time period to subset over"
            f"\n start time: {self.tuple[0]}"
            f"\n end time: {self.tuple[1]}"
        )
