from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from datetime import datetime
from contextlib import closing
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

from page_analyzer.validator import validate_url
from page_analyzer.seo_analyzer import get_url_data
from page_analyzer.database import (get_all_urls,
                                    get_urls_by_name,
                                    get_urls_by_id,
                                    get_url_checks,
                                    add_site,
                                    add_check)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def home():
       return render_template('index.html')

@app.get('/urls')
def urls_get():
    urls = get_all_urls()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'urls.html',
        urls=urls,
        messages=messages
    )

@app.post('/urls')
def urls_post():
    url = request.form.get('url')
    check = validate_url(url)

    url = check['url']
    error = check['error']

    if error:
        if error == 'exists':
            id_ = get_urls_by_name(url)['id']
            flash('Страница уже существует', 'alert-info')
            return redirect(url_for('url_show', id_=id_))
        
        flash('Некорректный URL', 'alert-danger')
        if error == 'zero':
            flash('URL обязателен', 'alert-danger')
        elif error == 'length':
            flash('URL превышает 255 символов', 'alert-danger')

        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', url=url, messages=messages), 422

    site = {
        'url': url,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    add_site(site)

    id_ = get_urls_by_name(url)['id']
    flash('Страница успешно добавлена', 'alert-success')
    return redirect(url_for('url_show', id_=id_))

@app.route('/urls/<int:id_>')
def url_show(id_):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM urls WHERE id = %s", (id_,))
        url = cur.fetchone()
    conn.close()

    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'urls.html',
        url=url,
        messages=messages
    )


if __name__ == '__main__':
    app.run()
