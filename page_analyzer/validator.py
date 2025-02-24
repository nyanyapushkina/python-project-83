import validators
from urllib.parse import urlparse
from page_analyzer.database import get_urls_by_name


def validate_url(url):
    if not url:
        return {'url': url, 'error': 'zero'}
    if len(url) > 255:
        return {'url': url, 'error': 'length'}
    if not validators.url(url):
        return {'url': url, 'error': 'invalid'}

    parsed_url = urlparse(url)
    norm_url = f'{parsed_url.scheme}://{parsed_url.netloc}'

    if get_urls_by_name(norm_url):
        return {'url': norm_url, 'error': 'exists'}

    return {'url': norm_url, 'error': None}