import validators
from urllib.parse import urlparse
from page_analyzer.database import get_urls_by_name
from page_analyzer.exceptions import (ZeroLengthError, TooLongError, 
                                      InvalidURLError, URLExistsError)


def validate_url(url: str) -> str:
    """
    Checks if a URL is valid and normalizes it.
    """
    if not url:
        raise ZeroLengthError('URL is required')

    if len(url) > 255:
        raise TooLongError('URL exceeds 255 characters')

    if not validators.url(url):
        raise InvalidURLError('Invalid URL')

    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise InvalidURLError('Invalid URL')

    norm_url = f'{parsed_url.scheme}://{parsed_url.netloc}'

    if get_urls_by_name(norm_url):
        raise URLExistsError('Page already exists', norm_url)

    return norm_url
