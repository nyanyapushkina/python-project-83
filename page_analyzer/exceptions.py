class ValidationError(Exception):
    """General Error"""
    pass

class ZeroLengthError(ValidationError):
    """Empty URL"""
    pass

class TooLongError(ValidationError):
    """More than 255 characters"""
    pass

class InvalidURLError(ValidationError):
    """Incorrect URL"""
    pass

class URLExistsError(ValidationError):
    """URL already exists"""
    pass