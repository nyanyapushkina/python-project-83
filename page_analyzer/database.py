from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from page_analyzer.config import Config
from page_analyzer.models import Site, UrlCheck

DATABASE_URL = Config.DATABASE_URL


def get_all_urls() -> list[Site]:
    """"
    Gets all URLs from the database. 
    Returns each URL's id, name, last check and status code. 
    """
    conn = connect(DATABASE_URL)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            q_select = '''SELECT DISTINCT ON (urls.id)
                            urls.id AS id,
                            urls.name AS name,
                            url_checks.created_at AS last_check,
                            url_checks.status_code AS status_code
                        FROM urls
                        LEFT JOIN url_checks ON urls.id = url_checks.url_id
                        AND url_checks.id = (SELECT MAX(id)
                                            FROM url_checks
                                            WHERE url_id = urls.id)
                        ORDER BY urls.id DESC;'''
            cur.execute(q_select)
            urls = cur.fetchall()
    finally:
        conn.close()

    sites = [Site(
        id=url['id'],
        url=url['name'],
        created_at=url.get('created_at'),
        last_check=url.get('last_check'),
        status_code=url.get('status_code')
    ) for url in urls]

    return sites


def get_urls_by_name(name: str) -> list[Site]:
    """"
    Gets all information about a certain URL by its name.
    """
    conn = connect(DATABASE_URL)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            q_select = '''SELECT * 
                        FROM urls 
                        WHERE name = %s'''
            cur.execute(q_select, (name,))
            urls = cur.fetchall()
    finally:
        conn.close()
    
    sites = [Site(id=url['id'], 
                  url=url['name'], 
                  created_at=url.get('created_at')) for url in urls]

    return sites


def get_urls_by_id(id_: int) -> Site:
    """"
    Gets all checks for a certain URL by its ID.
    """
    conn = connect(DATABASE_URL)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            q_select = '''SELECT *
                        FROM urls
                        WHERE id = %s'''
            cur.execute(q_select, (id_,))
            url = cur.fetchone()
    finally:
        conn.close()
    
    if url:
        return Site(id=url['id'], 
                    url=url['name'], 
                    created_at=url.get('created_at'))
    return None


def get_url_checks(id_: int) -> list[UrlCheck]:
    """"
    Gets all checks for a certain URL by its ID.
    """
    conn = connect(DATABASE_URL)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            q_select = '''SELECT * 
                        FROM url_checks 
                        WHERE url_id = %s 
                        ORDER BY id DESC '''
            cur.execute(q_select, (id_,))
            checks = cur.fetchall()
    finally:
        conn.close()

    return [UrlCheck(
        url_id=check['url_id'],
        status_code=check['status_code'],
        h1=check['h1'],
        title=check['title'],
        description=check['description'],
        created_at=check.get('created_at')
    ) for check in checks]


def add_site(site: Site) -> int:
    """"
    Adds a new URL to the database and returns its ID.
    """
    conn = connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            q_insert = '''INSERT 
                        INTO urls (name, created_at) 
                        VALUES (%s, NOW())
                        RETURNING id'''
            cur.execute(q_insert, (site.url,))
            site_id = cur.fetchone()[0]
            conn.commit()
            return site_id
    finally:
        conn.close()


def add_check(check: UrlCheck) -> UrlCheck:
    """"
    Adds a new check for a specific URL and returns the added check.
    """
    conn = connect(DATABASE_URL)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            q_insert = '''INSERT
                        INTO url_checks(
                            url_id,
                            status_code,
                            h1,
                            title,
                            description,
                            created_at)
                        VALUES (%s, %s, %s, %s, %s, NOW())
                        RETURNING *'''
            cur.execute(q_insert, (
                check.url_id,
                check.status_code,
                check.h1,
                check.title,
                check.description
            ))
            check_data = cur.fetchone()
            conn.commit()
            return UrlCheck(
                id=check_data['id'],
                url_id=check_data['url_id'],
                status_code=check_data['status_code'],
                h1=check_data['h1'],
                title=check_data['title'],
                description=check_data['description'],
                created_at=check_data['created_at']
            )
    finally:
        conn.close()
