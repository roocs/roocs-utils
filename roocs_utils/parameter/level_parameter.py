import numbers

from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue


class LevelParameter(_BaseParameter):

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
        return self._parse_levels()

    def asdict(self):
        return {"first_level": self.tuple[0], "last_level": self.tuple[1]}

    def __str__(self):
        return (
            f"Level range to subset over"
            f"\n first_level: {self.tuple[0]}"
            f"\n last_level: {self.tuple[1]}"
        )
