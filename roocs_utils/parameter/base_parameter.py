import collections

from roocs_utils.exceptions import InvalidParameterValue


class _BaseParameter(object):
    def __init__(self, input):
        self.input = input
        self.result = parse()
        self._validate()

    def _validate(self):
        raise NotImplementedError

    @property
    def raw(self):
        return self.input

    def _parse(self):
        if isinstance(self.input, self.__class__):
            return self.input

        if self.input is None:
            return self.input

        elif self.__class__ is TimeParameter or LevelParameter:
            return parse_range

        else:
            return parse_sequence

    def _parse_range(self):
        if self.input == '/':
            start = None
            end = None
        
        elif isinstance(self.input, str):
            if '/' not in input:
                raise InvalidParameterValue("The parameter should be passed in as a range separated by /")
            start = self.input.split('/')[0]
            end = self.input.split('/')[1]

        elif isinstance(self.input, collections.Sequence):
            if len(self.input) > 2:
                raise InvalidParameterValue(f"The parameter should be a range. Expected 2 values, "
                                            f"received {len(self.input)}")

            start = self.input[0]
            end = self.input[1]

        else:
            raise InvalidParameterValue(f"The parameter is not in an accepted format")

        return start, end

    def _parse_sequence(self, expected_length=None):
        if isinstance(self.input, str):
            sequence = self.input.split(',')

        elif isinstance(self.input, collections.Sequence):
            sequence = self.input

        else:
            raise InvalidParameterValue(f"The parameter is not in an accepted format")

        if expected:
            if len(sequence) != expected:
                raise InvalidParameterValue(f"The parameter should be of length {expected_length} but is of length"
                                            f"{len(sequence)}")

        return sequence

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return str(self)