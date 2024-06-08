from bs4 import BeautifulSoup


def parse_page(content):
    parsed_data = {}
    soup = BeautifulSoup(content, 'html.parser')

    h1 = soup.find('h1')
    parsed_data['h1'] = h1.get_text().strip() if h1 else ''

    title = soup.find('title')
    parsed_data['title'] = title.get_text().strip() if title else ''

    description = soup.find('meta', attrs={'name': 'description'})
    if description is None:
        parsed_data['description'] = ''
    else:
        parsed_data['description'] = description.get(
            'content', ''
        ).strip()

    return parsed_data
