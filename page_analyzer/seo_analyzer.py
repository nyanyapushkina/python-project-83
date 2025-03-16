import requests
from bs4 import BeautifulSoup


def get_html(url: str) -> str:
    """
    Gets HTML code of the webiste by its URL.
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        raise Exception(f"An error occured: {e}")


def parse_html(html: str) -> dict:
    """
    Gets elements of HTML-file (h1, title, and description).
    Returns a dictionary.
    """
    soup = BeautifulSoup(html, 'html.parser')

    h1_tag = soup.find('h1')
    title_tag = soup.find('title')
    description_tag = soup.find('meta', attrs={'name': 'description'})

    html_elements = {}

    html_elements['h1'] = h1_tag.text.strip() if h1_tag else ''
    html_elements['title'] = title_tag.text.strip() if title_tag else ''
    html_elements['description'] = description_tag['content'].strip() \
        if description_tag else ''
    
    return html_elements


def get_url_data(url: str) -> dict:
    """
    Gets data about a website by its URL.
    """
    try:
        html = get_html(url)
        parsed_data = parse_html(html)
        return {
            'status_code': 200,
            **parsed_data
        }
    except Exception as e:
        return {
            'error': str(e),
            'status_code': 502
        }
