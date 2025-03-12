from flask import (Blueprint,
                   flash,
                   get_flashed_messages,
                   redirect,
                   render_template,
                   request,
                   url_for)

from page_analyzer.validator import validate_url
from page_analyzer.exceptions import (ValidationError,
                                      ZeroLengthError, 
                                      TooLongError)
from page_analyzer.seo_analyzer import get_url_data
from page_analyzer.database import (get_all_urls,
                                    get_urls_by_name,
                                    get_urls_by_id,
                                    get_url_checks,
                                    add_site,
                                    add_check)

urls_bp = Blueprint('urls', __name__)


@urls_bp.route('', methods=['GET', 'POST'])
def urls():
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            norm_url = validate_url(url)

            existing_url = get_urls_by_name(norm_url)
            if existing_url:
                flash('Страница уже существует', 'alert-info')
                return redirect(url_for('urls.url_show', 
                                        id_=existing_url[0]['id']))

            site = {
                'url': norm_url
            }
            add_site(site)

            url_data = get_urls_by_name(norm_url)
            if url_data:
                id_ = url_data[0]['id']
                flash('Страница успешно добавлена', 'alert-success')
                return redirect(url_for('urls.url_show', id_=id_))
            else:
                flash('Ошибка при добавлении страницы', 'alert-danger')
                return redirect(url_for('main.home'))

        except ValidationError as e:
            if isinstance(e, ZeroLengthError):
                flash('URL обязателен', 'alert-danger')
            elif isinstance(e, TooLongError):
                flash('URL превышает 255 символов', 'alert-danger')
            else:
                flash('Некорректный URL', 'alert-danger')

            messages = get_flashed_messages(with_categories=True)

            return render_template('index.html', 
                                   url=url, 
                                   messages=messages), 422
    
    else:
        urls = get_all_urls()
        messages = get_flashed_messages(with_categories=True)
        return render_template('urls.html', 
                               urls=urls, 
                               messages=messages)


@urls_bp.route('/<int:id_>')
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
        return redirect(url_for('main.page_not_found'))


@urls_bp.route('/<int:id_>/checks', methods=['POST'])
def url_check(id_):
    url = get_urls_by_id(id_)['name']

    check = get_url_data(url)

    if check is None or 'error' in check:
        flash('Произошла ошибка при проверке', 'alert-danger')
    else:
        check['url_id'] = id_
        add_check(check)
        flash('Страница успешно проверена', 'alert-success')

    return redirect(url_for('urls.url_show', id_=id_))
