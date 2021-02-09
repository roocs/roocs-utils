from collections.abc import Sequence
from pydoc import locate

from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.exceptions import MissingParameterValue
from roocs_utils.utils.file_utils import FileMapper


class _BaseParameter(object):
    """
    Base class for parameters used in operations (e.g. subset, average etc.)
    """

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

        elif isinstance(self.input, Sequence):
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

        if self.input in (None, ""):
            sequence = None

        # check str or bytes
        elif isinstance(self.input, (str, bytes)):
            sequence = [x.strip() for x in self.input.split(",")]

        elif isinstance(self.input, FileMapper):
            return [self.input]

        elif isinstance(self.input, Sequence):
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
