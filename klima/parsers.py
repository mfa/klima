import datetime

from bs4 import BeautifulSoup


def parse_lubw(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    name = soup.find(id="Name").text.replace('(vorläufige Daten)', '').replace('\xa0', ' ').strip()
    date = datetime.datetime.strptime(soup.find(id="Datum").text.strip(), '%d.%m.%Y %H:%M')
    last_component = ''
    elements = []
    for row in soup.find(id="WerteTabelle").find_all('tr'):
        data = {
            'date': date,
            'name': name,
        }
        add = 0
        keys = ['component', 'timespan', 'current_value', 'maximum_value']
        for index, cell in enumerate(row.find_all('td')):
            content = cell.text.strip().replace('\xa0', ' ')
            if 'Std.' in content and index == 0:
                data[keys[index]] = last_component
                add = 1
            if len(keys) > (index+add):
                data[keys[index+add]] = content
        last_component = data.get('component')
        if len(data.keys()) > 2:
            elements.append(data)
    return elements
