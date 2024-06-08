import os
from datetime import datetime

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import NamedTupleCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


class DBConnection:
    def __enter__(self):
        self.connection = psycopg2.connect(DATABASE_URL)
        self.cursor = self.connection.cursor(cursor_factory=NamedTupleCursor)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()


def get_url_by_id(url_id):
    with DBConnection() as cursor:
        query = "SELECT * FROM urls WHERE id = %s"
        cursor.execute(query, (url_id,))
        url = cursor.fetchone()
        return url


def get_url_by_name(url_name):
    with DBConnection() as cursor:
        query = "SELECT * FROM urls WHERE name = %s"
        cursor.execute(query, (url_name,))
        data = cursor.fetchone()
        return data


def get_checks_by_url_id(url_id):
    with DBConnection() as cursor:
        query = "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC"
        cursor.execute(query, (url_id,))
        return cursor.fetchall()


def get_all_urls():
    with DBConnection() as cursor:
        query = "SELECT * FROM urls ORDER BY id DESC;"
        checks_query = '''SELECT
                        url_id,
                        status_code,
                        MAX(created_at) as created_at
                        FROM url_checks
                        GROUP BY url_id, status_code
                        ORDER BY created_at'''
        cursor.execute(query)
        urls = cursor.fetchall()
        cursor.execute(checks_query)
        checks = {item.url_id: item for item in cursor.fetchall()}
        urls_list = []
        for url in urls:
            url_data = {
                'id': url.id,
                'name': url.name,
            }
            check = checks.get(url.id)
            if check:
                url_data['status_code'] = check.status_code
                url_data['last_check'] = check.created_at
            urls_list.append(url_data)

        return urls_list


def add_url(url_name):
    with DBConnection() as cursor:
        query = '''INSERT INTO urls (name, created_at)
                VALUES (%s, %s) RETURNING id'''
        cursor.execute(query, (url_name, datetime.now()))
        return cursor.fetchone().id


def add_url_check(check_data):
    with DBConnection() as cursor:
        query = ('INSERT INTO url_checks '
                 '(url_id, status_code, h1, title, description, created_at) '
                 'VALUES (%s, %s, %s, %s, %s, %s)')
        values = (check_data.get('url_id'), check_data.get('status_code'),
                  check_data.get('h1', ''), check_data.get('title', ''),
                  check_data.get('description', ''), datetime.now())
        cursor.execute(query, values)
