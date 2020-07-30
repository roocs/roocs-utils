from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue


class LevelParameter(_BaseParameter):

    def _validate(self):
        if not isinstance(self.input, tuple):
            raise InvalidParameterValue('The level parameter should be passed in as a tuple')

        """
        Other things to check:
        - starts with / or number
        - ends with / or Z or number
        - format of datetime
        """

    @property
    def str(self):
        return str(self.input)
