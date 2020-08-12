from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue


class LevelParameter(_BaseParameter):

    parse_method = '_parse_range'

    def _validate(self):
        self._parse_levels()

    def _parse_levels(self):
        # should this default to the start and end levels of the data?
        start, end = self._result

        for value in self._result:
            if value is None:
                pass
            elif isinstance(value, str):
                if not value.replace('.', '', 1).isdigit():
                    raise InvalidParameterValue("Level values must be a number")
            else:
                if not (isinstance(value, float) or isinstance(value, int)):
                    raise InvalidParameterValue("Level values must be a number")

            # convert to floats?
            if start is not None:
                start = float(start)
            if end is not None:
                end = float(end)

        return start, end

    @property
    def tuple(self):
        if self._parse_levels() is not (None, None):
            return self._parse_levels()

    def asdict(self):
        if self.tuple is not None:
            return {"start": self.tuple[0],
                    "end": self.tuple[1]}

    def __str__(self):
        return f'Level range to subset over' \
               f'\n start: {self.tuple[0]}' \
               f'\n end: {self.tuple[1]}'
