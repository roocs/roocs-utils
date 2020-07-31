from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue

from dateutil import parser as date_parser


class TimeParameter(_BaseParameter):

    def _validate(self):
        try:
            self.parse_times()

        except parser._parser.ParserError:
            raise InvalidParameterValue("Unable to parse the time values entered")

    def _parse_times(self):
        if len(self.result) > 1:
            start, end = self.result

            start_time = date_parser.parse(start).isoformat()
            end_time = date_parser.parse(end).isoformat()

            return start_time, end_time

        else:
            return self.result

    def asdict(self):
        return dict(self._parse_times)

    @property
    def tuple(self):
        return self._parse_times

    def __str__(self):
        return f'Time period to subset over' \
               f'\n start time: ' \
               f'\n end time:'