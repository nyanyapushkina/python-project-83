class ValidationError(Exception):

    """General Error"""
    pass


class ZeroLengthError(ValidationError):

    """Empty URL"""
    pass


class TooLongError(ValidationError):

    """URL is too long"""
    pass


class InvalidURLError(ValidationError):

    """Incorrect URL"""
    pass
