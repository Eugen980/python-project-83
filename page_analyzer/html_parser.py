from bs4 import BeautifulSoup


def parse_page(content):
    soup = BeautifulSoup(content, 'html.parser')

    h1 = soup.find('h1')
    title = soup.find('title')
    description = soup.find('meta', attrs={'name': 'description'})

    return {
        'h1': h1.get_text().strip() if h1 else '',
        'title': title.get_text().strip() if title else '',
        'description': description.get(
            'content', ''
        ).strip() if description else ''
    }
