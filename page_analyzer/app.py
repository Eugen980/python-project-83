import os

import validators
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, flash, url_for

from db import (get_url_by_id, get_url_by_name, get_checks_by_url_id,
                add_url, get_all_urls, add_url_check)


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def get_urls():
    if request.method == 'POST':
        url_name = request.form['url']
        if validators.url(url_name) is True:
            url = get_url_by_name(url_name)
            if url:
                flash('Страница уже существует', category='alert-info')
                url_id = url.id
                return redirect(url_for('get_url', url_id=url_id))
            else:
                url_id = add_url(url_name)
                flash('Страница успешно добавлена', category='alert-success')
                return redirect(url_for('get_url', url_id=url_id))
        else:
            flash('Некорректный URL', category='alert-danger')
            return redirect(url_for('index'))
    urls = get_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:url_id>')
def get_url(url_id):
    url = get_url_by_id(url_id)
    if url is None:
        pass
    checks = get_checks_by_url_id(url_id)
    return render_template('url_page.html', url=url, checks=checks)


@app.route('/urls/<int:url_id>/checks', methods=['POST'])
def url_checks(url_id):
    add_url_check(url_id)
    flash('Страница успешна проверена', 'alert-success')
    return redirect(url_for('get_url', url_id=url_id))


if __name__ == '__main__':
    app.run(debug=True)
