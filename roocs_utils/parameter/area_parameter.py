from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue


class AreaParameter(_BaseParameter):
    def _validate(self):
        if not isinstance(self.input, str):
            raise InvalidParameterValue("Area parameter must be passed as a string")


    @property
    def tuple(self):
        values = []

        for value in self.input.split(','):
            value = float(value)
            values.append(value)

        return tuple(values)