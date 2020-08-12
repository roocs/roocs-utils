import collections
from pydoc import locate

from roocs_utils.exceptions import InvalidParameterValue, MissingParameterValue


class _BaseParameter(object):

    parser_method = "UNDEFINED"

    def __init__(self, input):
        self.input = input
        self._result = self._parse()
        self._validate()

    def _validate(self):
        raise NotImplementedError

    @property
    def raw(self):
        return self.input

    def _parse(self):
        if isinstance(self.input, self.__class__):
            return self.input._parse()

        else:
            return getattr(self, self.parse_method)()

    def _parse_range(self):
        if self.input in ("/", None, ""):
            start = None
            end = None

        elif isinstance(self.input, str):
            if "/" not in self.input:
                raise InvalidParameterValue(
                    f"{self.__class__.__name__} should be passed in as a range separated by /"
                )

            # empty string either side of '/' is converted to None
            start, end = [x.strip() or None for x in self.input.split("/")]

        elif isinstance(self.input, collections.Sequence):
            if len(self.input) != 2:
                raise InvalidParameterValue(
                    f"{self.__class__.__name__} should be a range. Expected 2 values, "
                    f"received {len(self.input)}"
                )

            start, end = self.input

        else:
            raise InvalidParameterValue(
                f"{self.__class__.__name__} is not in an accepted format"
            )
        return start, end

    def _parse_sequence(self):
        # check str or bytes
        if self.input in (None, ""):
            sequence = None

        elif isinstance(self.input, (str, bytes)):
            sequence = [x.strip() for x in self.input.split(",")]

        elif isinstance(self.input, collections.Sequence):
            sequence = self.input

        else:
            raise InvalidParameterValue(
                f"{self.__class__.__name__} is not in an accepted format"
            )

        return sequence

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return str(self)
