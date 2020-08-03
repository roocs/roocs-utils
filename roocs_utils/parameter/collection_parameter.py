from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue


class CollectionParameter(_BaseParameter):

    def _validate(self):
        self._parse_ids()

    def _parse_ids(self):
        for value in self._result:
            if not isinstance(value, str):
                raise InvalidParameterValue("Each id must be a string")

        return tuple(self._result)

    @property
    def tuple(self):
        return self._parse_ids()

    def __str__(self):
        string = 'Datasets to analyse:'
        for i in self.tuple:
            string += f'\n{i}'
        return string
