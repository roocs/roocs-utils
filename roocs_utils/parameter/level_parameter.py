from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue


class LevelParameter(_BaseParameter):

    def _validate(self):
        if not isinstance(self.input, int):
            raise InvalidParameterValue("Levels should be passed in as integers")

    @property
    def str(self):
        return str(self.input)
