import psycopg2
from psycopg2.extras import NamedTupleCursor


class DBConnection:
    def __init__(self, app):
        self.app = app

    @staticmethod
    def exec_with_in_db(func):
        def inner(self, *args, commit=False, **kwargs):
            try:
                with psycopg2.connect(self.app.config['DATABASE_URL']) as conn:     # noqa: 501
                    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:    # noqa: 501
                        result = func(self, cursor, *args, **kwargs)
                        if commit:
                            conn.commit()
                        return result
            except psycopg2.Error as e:
                raise e
        return inner

    @exec_with_in_db
    def get_url_by_id(self, cursor, url_id):
        query = "SELECT * FROM urls WHERE id = %s"
        cursor.execute(query, (url_id,))
        url = cursor.fetchone()
        return url

    @exec_with_in_db
    def get_url_by_name(self, cursor, url_name):
        query = "SELECT * FROM urls WHERE name = %s"
        cursor.execute(query, (url_name,))
        data = cursor.fetchone()
        return data

    @exec_with_in_db
    def get_checks_by_url_id(self, cursor, url_id):
        query = "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC"
        cursor.execute(query, (url_id,))
        return cursor.fetchall()

    @exec_with_in_db
    def get_all_urls(self, cursor):
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

    @exec_with_in_db
    def add_url(self, cursor, url_name, commit=True):
        query = '''INSERT INTO urls (name)
                VALUES (%s) RETURNING id'''
        cursor.execute(query, (url_name,))
        return cursor.fetchone().id

    @exec_with_in_db
    def add_url_check(self, cursor, check_data, commit=True):
        query = ('INSERT INTO url_checks '
                 '(url_id, status_code, h1, title, description) '
                 'VALUES (%s, %s, %s, %s, %s)')
        values = (check_data.get('url_id'), check_data.get('status_code'),
                  check_data.get('h1', ''), check_data.get('title', ''),
                  check_data.get('description', ''))
        cursor.execute(query, values)
