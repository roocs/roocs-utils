from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue


class LevelParameter(_BaseParameter):


    @property
    def str(self):
        return str(self.input)

    def __str__(self):
        return f'Level range to subset over' \
               f'\n start: ' \
               f'\n end:'
