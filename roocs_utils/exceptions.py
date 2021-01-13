class InvalidParameterValue(Exception):
    pass


class MissingParameterValue(Exception):
    pass


class InvalidProject(Exception):
    """ Raised when the project is unknown to roocs.ini """


class InconsistencyError(Exception):
    """Raised when there is some inconsistency which prevents files
    being scanned."""
