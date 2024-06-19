from bs4 import BeautifulSoup


def truncate(text):
    return f'{text[:255]}...' if len(text) > 255 else text


def parse_page(content):
    soup = BeautifulSoup(content, 'html.parser')

    h1 = soup.find('h1')
    title = soup.find('title')
    description = soup.find('meta', attrs={'name': 'description'})

    return {
        'h1': h1.text[:255] if h1 else '',
        'title': title.text[:255] if title else '',
        'description': truncate(description.get(
            'content', ''
        )) if description else ''
    }
