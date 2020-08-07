from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue


class AreaParameter(_BaseParameter):

    parse_method = '_parse_sequence'
    expected_length = 4

    def _validate(self):
        self._parse_values()

    def _parse_values(self):
        area = []
        for value in self._result:
            if isinstance(value, str):
                if not value.replace('.', '', 1).isdigit():
                    raise InvalidParameterValue("Area values must be a number")
            else:
                if not (isinstance(value, float) or isinstance(value, int)):
                    raise InvalidParameterValue("Area values must be a number")

            area.append(float(value))

        return tuple(area)

    def asdict(self):
        return {"lon_bnds": [self.tuple[0],self.tuple[2]],
                "lat_bnds": [self.tuple[1], self.tuple[3]]}

    @property
    def tuple(self):
        return self._parse_values()

    def __str__(self):
        return f'Area to subset over:' \
               f'\n {self.tuple}'
