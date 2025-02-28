from flask import (Flask,
                   flash,
                   get_flashed_messages,
                   redirect,
                   render_template,
                   request,
                   url_for)
from datetime import datetime
from dotenv import load_dotenv

import os

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
app.secret_key = os.getenv('SECRET_KEY')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


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
            url_data = get_urls_by_name(url)
            if url_data:
                id_ = url_data[0]['id']
                flash('Страница уже существует', 'alert-info')
                return redirect(url_for('url_show', id_=id_))
            else:
                flash('Страница не найдена', 'alert-danger')
                return redirect(url_for('home'))
        else:
            flash('Некорректный URL', 'alert-danger')

            if error == 'zero':
                flash('URL обязателен', 'alert-danger')
            elif error == 'length':
                flash('URL превышает 255 символов', 'alert-danger')

            messages = get_flashed_messages(with_categories=True)
            return render_template('index.html', 
                                   url=url, 
                                   messages=messages), 422
    
    else:
        site = {
            'url': url,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        add_site(site)

        url_data = get_urls_by_name(url)
        if url_data:
            id_ = url_data[0]['id']
            flash('Страница успешно добавлена', 'alert-success')
            return redirect(url_for('url_show', id_=id_))
        else:
            flash('Ошибка при добавлении страницы', 'alert-danger')
            return redirect(url_for('home'))


@app.route('/urls/<int:id_>')
def url_show(id_):
    url = get_urls_by_id(id_)
    checks = get_url_checks(id_)
    messages = get_flashed_messages(with_categories=True)
    
    if url:
        return render_template(
            'url.html',
            url=url,
            checks=checks,
            messages=messages
        )
    else:
        return redirect(url_for('page_not_found'))


@app.post('/urls/<int:id_>/checks')
def url_check(id_):
    url = get_urls_by_id(id_)['name']

    check = get_url_data(url)
    
    if check is None or 'error' in check:
        flash('Произошла ошибка при проверке', 'alert-danger')
        
    else:
        check['url_id'] = id_
        check['checked_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        add_check(check)
        flash('Страница успешно проверена', 'alert-success')
    
    return redirect(url_for('url_show', id_=id_))
