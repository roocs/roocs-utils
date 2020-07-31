
class _BaseParameter(object):
    def __init__(self, input):
        self.input = input
        self._validate()

    def _validate(self):
        raise NotImplementedError

    @property
    def raw(self):
        return self.input

    @property
    def __unicode__(self):
        return f'An object of the {self.__class__.__name__} class'

    @property
    def __repr__(self):
        return str(self.__unicode__)

    @property
    def __str__(self):
        return str(self.__unicode__)