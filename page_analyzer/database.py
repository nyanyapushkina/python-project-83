from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from page_analyzer.config import Config

DATABASE_URL = Config.DATABASE_URL


def get_all_urls():
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

    return urls


def get_urls_by_name(name):
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

    return urls


def get_urls_by_id(id_):
    conn = connect(DATABASE_URL)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            q_select = '''SELECT *
                        FROM urls
                        WHERE id = %s'''
            cur.execute(q_select, (id_,))
            urls = cur.fetchone()
    finally:
        conn.close()

    return urls


def get_url_checks(id_):
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

    return checks


def add_site(site):
    conn = connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            q_insert = '''INSERT 
                        INTO urls (name, created_at) 
                        VALUES (%s, NOW())'''
            cur.execute(q_insert, (site['url'],))
            conn.commit()
    finally:
        conn.close()


def add_check(check):
    conn = connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            q_insert = '''INSERT
                        INTO url_checks(
                            url_id,
                            status_code,
                            h1,
                            title,
                            description,
                            created_at)
                        VALUES (%s, %s, %s, %s, %s, NOW())'''
            cur.execute(q_insert, (
                check['url_id'],
                check['status_code'],
                check['h1'],
                check['title'],
                check['description']
            ))
            conn.commit()
    finally:
        conn.close()
