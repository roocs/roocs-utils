from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue, MissingParameterValue


class CollectionParameter(_BaseParameter):

    parse_method = "_parse_sequence"

    def _validate(self):
        if self._result is None:
            raise MissingParameterValue(f"{self.__class__.__name__} must be provided")

        self._parse_ids()

    def _parse_ids(self):
        for value in self._result:
            if not isinstance(value, str):
                raise InvalidParameterValue("Each id in a collection must be a string")

        return tuple(self._result)

    @property
    def tuple(self):
        return self._parse_ids()

    def __str__(self):
        string = "Datasets to analyse:"
        for i in self.tuple:
            string += f"\n{i}"
        return string
