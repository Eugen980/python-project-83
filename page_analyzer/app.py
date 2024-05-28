import os
from datetime import datetime
import validators
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, flash, url_for


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls/<id>')
def get_url(id):
    connect = psycopg2.connect(db)
    cursor = connect.cursor()
    cursor.execute(
        '''SELECT name, created_at FROM urls WHERE id = %s''', (id,)
        )
    data = cursor.fetchall()[0]
    name = data[0]
    time = data[1]
    cursor.close()
    connect.close()
    return render_template(
        'url_page.html',
        id=id, name=name,
        created_time=time)


@app.route('/urls', methods=['GET', 'POST'])
def get_urls():
    connect = psycopg2.connect(db)
    cursor = connect.cursor()
    if request.method == 'POST':
        current_url = request.form['url']
        if validators.url(current_url) is True:
            cursor.execute(
                '''SELECT name
                FROM urls WHERE name = %s''', (current_url,))
            if cursor.fetchone():
                flash('Страница уже существует', category='alert-info')
                cursor.execute(
                    "SELECT id, name, created_at FROM urls WHERE name = %s",
                    (current_url,)
                    )
                cur_id = cursor.fetchone()[0]
                return redirect(url_for('get_url', id=cur_id))
            else:
                cursor.execute(
                   '''INSERT INTO urls (name, created_at) VALUES (%s, %s)''',
                   (current_url, datetime.now())
                )
                connect.commit()
                cursor.execute(
                    "SELECT id, name, created_at FROM urls WHERE name = %s",
                    (current_url,)
                    )
                cur_id = cursor.fetchone()[0]
                flash('Страница успешно добавлена', category='alert-success')
                return redirect(url_for('get_url', id=cur_id))
        else:
            flash('Некорректный URL', category='alert-danger')
            return redirect(url_for('index'))
    cursor.execute("SELECT * FROM urls ORDER BY id DESC")
    urls = cursor.fetchall()
    cursor.close()
    connect.close()
    return render_template('urls.html', urls=urls)


if __name__ == '__main__':
    app.run(debug=True)
