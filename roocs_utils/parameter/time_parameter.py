from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue

import re

class TimeParameter(_BaseParameter):

    def _validate(self):
        if not isinstance(self.input, str):
            raise InvalidParameterValue("The time period should be passed in as a string")

        pattern = re.compile(r'^(\d+)(?::([0-5]?\d)(?::([0-5]?\d))?)?$')
        if not pattern.match:
            raise InvalidParameterValue("The time string is not formatted correctly")
        """
        Other things to check:
        - starts with / or number
        - ends with / or Z or number
        - format of datetime
        """

    @property
    def tuple(self):
        start = self.input.split('/')[0]
        end = self.input.split('/')[1]
        return start, end

