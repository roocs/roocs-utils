from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.exceptions import InvalidParameterValue


class CollectionParameter(_BaseParameter):
    
    def _validate(self):
        if not isinstance(self.input, list):
            if not isinstance(self.input, tuple):
                raise InvalidParameterValue("Collections must be a list or tuple")
        for id in self.input:
            if not isinstance(id, str):
                raise InvalidParameterValue("Each id must be a string")