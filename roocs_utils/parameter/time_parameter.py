from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue


class TimeParameter(_BaseParameter):

    def _validate(self):
        if not isinstance(self.input, str):
            raise InvalidParameterValue('The time period should be passed in as a string')

        """
        Other things to check:
        - starts with / or number
        - ends with / or Z or number
        - format of datetime
        """

    @property
    def tuple(self):
        start = self.input.split('/')[0]
        end = self.input.split('')[1]
        return tuple(start, end)

