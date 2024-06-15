from validators import url
from urllib.parse import urlparse


def is_valid(url_name):
    return url(url_name)


def normalize(url_name):
    url = urlparse(url_name)
    return url.scheme + '://' + url.hostname
