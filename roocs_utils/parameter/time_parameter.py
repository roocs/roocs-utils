from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue

from dateutil import parser as date_parser


class TimeParameter(_BaseParameter):

    def _validate(self):
        try:
            self._parse_times()

        except (date_parser._parser.ParserError, TypeError):
            raise InvalidParameterValue("Unable to parse the time values entered")

    def _parse_times(self):
        # should this default to the start and end time of the data?
        start, end = self._result

        if start is not None:
            start = date_parser.parse(start).isoformat()
        if end is not None:
            end = date_parser.parse(end).isoformat()

        return start, end

    def asdict(self):

        return {"start_time": self.tuple[0],
                "end_time": self.tuple[1]}

    @property
    def tuple(self):
        return self._parse_times()

    def __str__(self):
        return f'Time period to subset over' \
               f'\n start time: {self.tuple[0]}' \
               f'\n end time: {self.tuple[1]}'