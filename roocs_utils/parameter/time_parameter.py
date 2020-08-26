from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue

from dateutil import parser as date_parser
import datetime


class TimeParameter(_BaseParameter):

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
            start = (
                date_parser.parse(start, default=datetime.datetime(2005, 1, 1))
                .isoformat()
                .split("-")[0]
            )
        if end is not None:
            end = (
                date_parser.parse(end, default=datetime.datetime(2005, 12, 30))
                .isoformat()
                .split("-")[0]
            )

        return start, end

    @property
    def tuple(self):
        if self._parse_times() is not (None, None):
            return self._parse_times()

    # was start/end time - changed to date as xclim uses date
    def asdict(self):
        if self.tuple is not None:
            return {"start_time": self.tuple[0], "end_time": self.tuple[1]}

    def __str__(self):
        return (
            f"Time period to subset over"
            f"\n start time: {self.tuple[0]}"
            f"\n end time: {self.tuple[1]}"
        )
