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
        raise ZeroLengthError('URL обязателен')

    if len(url) > 255:
        raise TooLongError('URL превышает 255 символов')

    if not validators.url(url):
        raise InvalidURLError('Некорректный URL')

    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise InvalidURLError('Некорректный URL')

    norm_url = f'{parsed_url.scheme}://{parsed_url.netloc}'

    if get_urls_by_name(norm_url):
        raise URLExistsError('Страница уже существует', norm_url)

    return norm_url
