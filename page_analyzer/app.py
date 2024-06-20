import os

import requests
from dotenv import load_dotenv
from flask import (
    Flask, render_template,
    redirect, request, flash, url_for, abort
    )

from page_analyzer.utils import validate_url, normalize
from page_analyzer.html_parser import parse_page
from page_analyzer.db import DBConnection


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

db_manager = DBConnection(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_urls():
    url = request.form.get('url')
    normal_url = normalize(url)
    validation_error = validate_url(normal_url)

    if validation_error:
        flash(validation_error, category='alert-danger')
        return render_template('index.html'), 422

    url = db_manager.get_url_by_name(normal_url)
    if url:
        flash('Страница уже существует', category='alert-info')
        url_id = url.id
        return redirect(url_for('get_url', url_id=url_id))

    url_id = db_manager.add_url(normal_url)
    flash('Страница успешно добавлена', category='alert-success')
    return redirect(url_for('get_url', url_id=url_id))


@app.get('/urls')
def get_urls():
    urls = db_manager.get_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:url_id>')
def get_url(url_id):
    url = db_manager.get_url_by_id(url_id)
    if url is None:
        abort(404)
    checks = db_manager.get_checks_by_url_id(url_id)
    return render_template('url_page.html', url=url, checks=checks)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/error404.html'), 404


@app.post('/urls/<int:url_id>/checks')
def url_checks(url_id):
    url = db_manager.get_url_by_id(url_id)
    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
        return redirect(url_for('get_url', url_id=url_id))

    check_data = parse_page(response.text)
    check_data['url_id'] = url_id
    check_data['status_code'] = response.status_code

    db_manager.add_url_check(check_data)
    flash('Страница успешно проверена', 'alert-success')
    return redirect(url_for('get_url', url_id=url_id))


if __name__ == '__main__':
    app.run(debug=True)
