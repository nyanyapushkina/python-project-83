import validators
from urllib.parse import urlparse
from page_analyzer.exceptions import (ZeroLengthError, TooLongError, 
                                      InvalidURLError)


MAX_LENGTH = 255


def validate_url(url: str) -> str:
    """
    Checks if a URL is valid and normalizes it.
    """
    if not url:
        raise ZeroLengthError()

    if len(url) > MAX_LENGTH:
        raise TooLongError()

    if not validators.url(url):
        raise InvalidURLError()

    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise InvalidURLError()

    norm_url = f'{parsed_url.scheme}://{parsed_url.netloc}'

    return norm_url
