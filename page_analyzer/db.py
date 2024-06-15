import os

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import NamedTupleCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def cursor(method):
    def wrapper(self, *args):
        self.connection = psycopg2.connect(DATABASE_URL)
        self.cursor = self.connection.cursor(cursor_factory=NamedTupleCursor)
        result = method(self, *args)
        self.cursor.close()
        self.connection.commit()
        self.connection.close()
        return result
    return wrapper


class DBConnection:

    @cursor
    def get_url_by_id(self, url_id):
        query = "SELECT * FROM urls WHERE id = %s"
        self.cursor.execute(query, (url_id,))
        url = self.cursor.fetchone()
        return url

    @cursor
    def get_url_by_name(self, url_name):
        query = "SELECT * FROM urls WHERE name = %s"
        self.cursor.execute(query, (url_name,))
        data = self.cursor.fetchone()
        return data

    @cursor
    def get_checks_by_url_id(self, url_id):
        query = "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC"
        self.cursor.execute(query, (url_id,))
        return self.cursor.fetchall()

    @cursor
    def get_all_urls(self):
        query = "SELECT * FROM urls ORDER BY id DESC;"
        checks_query = '''SELECT
                        url_id,
                        status_code,
                        MAX(created_at) as created_at
                        FROM url_checks
                        GROUP BY url_id, status_code
                        ORDER BY created_at'''
        self.cursor.execute(query)
        urls = self.cursor.fetchall()
        self.cursor.execute(checks_query)
        checks = {item.url_id: item for item in self.cursor.fetchall()}
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

    @cursor
    def add_url(self, url_name):
        query = '''INSERT INTO urls (name)
                VALUES (%s) RETURNING id'''
        self.cursor.execute(query, (url_name,))
        return self.cursor.fetchone().id

    @cursor
    def add_url_check(self, check_data):
        query = ('INSERT INTO url_checks '
                 '(url_id, status_code, h1, title, description) '
                 'VALUES (%s, %s, %s, %s, %s)')
        values = (check_data.get('url_id'), check_data.get('status_code'),
                  check_data.get('h1', ''), check_data.get('title', ''),
                  check_data.get('description', ''))
        self.cursor.execute(query, values)
