# from clisops
class InvalidParameterValue(Exception):
    pass


class MissingParameterValue(Exception):
    pass


# from dachar
class InconsistencyError(Exception):
    """Raised when there is some inconsistency which prevents files
    being scanned."""
