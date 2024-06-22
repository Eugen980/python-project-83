from validators import url
from urllib.parse import urlparse


def validate_url(url_name):
    if not url_name:
        return 'URL обязателен к заполнению'
    elif not url(url_name):
        return 'Некорректный URL'
    elif len(url_name) > 255:
        return 'Введенный URL превышает допустимую длину символов'


def normalize(url_name):
    url = urlparse(url_name)
    return f'{url.scheme}://{url.hostname}'
