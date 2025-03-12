from flask import (Blueprint,
                   flash,
                   get_flashed_messages,
                   render_template,
                   request)
from page_analyzer.exceptions import (ValidationError,
                                      ZeroLengthError, 
                                      TooLongError)

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    return render_template('index.html')


@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    if isinstance(e, ZeroLengthError):
        flash('URL обязателен', 'alert-danger')
    elif isinstance(e, TooLongError):
        flash('URL превышает 255 символов', 'alert-danger')
    else:
        flash('Некорректный URL', 'alert-danger')

    messages = get_flashed_messages(with_categories=True)

    return render_template('index.html', 
                           url=request.form.get('url'), 
                           messages=messages), 422
