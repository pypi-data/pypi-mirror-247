class BaseError(Exception):
    """
    Base class for all errors
    """


class QuantityError(BaseError):
    """
    Base class for all quantity-related errors
    """


# TODO Olessya @Paul: should we rename to QuantityMagnitudeError to stay consistent with API?
class QuantityValueError(QuantityError):
    """
    Class for errors related to quantity values
    """


class QuantityUnitsError(QuantityError):
    """
    Class for errors related to quantity units
    """


class ParameterError(BaseError):
    """
    Base class for all parameter-related errors
    """


class ParameterValueError(BaseError):
    """
    Class for errors related to (user-given) parameter values
    """
