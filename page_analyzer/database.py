import os
from contextlib import closing
from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def show_all_urls():
    conn = connect(DATABASE_URL)
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
    conn.close()

    return urls

def get_urls_by_name(url):
    conn = connect(DATABASE_URL)
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id FROM urls WHERE name = %s", (url,))
        url_data = cur.fetchone()
    conn.close()
    return url_data


def add_site(site):
    conn = connect(DATABASE_URL)
    with conn.cursor() as cur:
        cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)", (site['url'], site['created_at']))
        conn.commit()
    conn.close()
