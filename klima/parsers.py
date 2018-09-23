import datetime
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup


def parse_lubw(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    name = soup.find(id="Name").text
    name = name.replace('(vorläufige Daten)', '').replace('\xa0', ' ')
    name = name.replace('(V)', '').replace('*)', '').strip()
    date = datetime.datetime.strptime(soup.find(id="Datum").text.strip(), '%d.%m.%Y %H:%M')
    last_component = ''
    elements = []
    data = {
        'date': date,
        'name': name,
    }
    for row in soup.find(id="WerteTabelle").find_all('tr'):
        d = {}
        add = 0
        keys = ['component', 'timespan', 'current_value', 'maximum_value']
        for index, cell in enumerate(row.find_all('td')):
            content = cell.text.strip().replace('\xa0', ' ')
            if 'Std.' in content and index == 0:
                d[keys[index]] = last_component
                add = 1
            if len(keys) > (index+add):
                d[keys[index+add]] = content
        last_component = d.get('component')
        if len(d.keys()) > 2:
            elements.append(d)
    data['items'] = elements
    return data


def parse_stadtklima_stgt(html_string):
    html_string = html_string.decode('utf-8', 'ignore')

    key_mapping = {
        '(NO)': 'NO',
        '(NO2)': 'NO2',
        '(O3)': 'O3',
        '(O3)': 'O3',
        '(O3 + NO2)': 'O3+NO2',
        '(PM10)': 'PM10',
        '(PM2.5)': 'PM2.5',
        'Lufttemperatur': 'temperature',
        'Empfundene Temperatur in der Sonne': 'felt temperature - sun',
        'Empfundene Temperatur im Schatter': 'felt temperature - shadow',
        'Empfundene Temperatur mit Windchill-Effekt': 'felt temperature - windchill',
        'Windgeschwindigkeit': 'wind speed',
        'Windrichtung': 'wind direction',
        'Relative Luftfeuchte': 'humidity',
        'Absoluter Luftdruck': 'air presure (absolute)',
        'Relativer Luftdruck': 'air presure (relative)',
        'Niederschlag': 'precipitation',
        'Globalstrahlung': 'global radiation',
        'Strahlungsbilanz': 'radiation balance',
        'UV-A Strahlung': 'radiation (UV-A)',
        'UV-B Strahlung': 'radiation (UV-B)',
    }

    data = {
        'name': 'Mitte--Schwabenzentrum'
    }
    # because of bad html, this is not done using bs4
    this_key = None
    for line in html_string.split('\n'):
        soup = BeautifulSoup(line, 'html.parser')
        text = soup.text.strip()
        line = line.replace("'", '"')
        if line.startswith('<td align="left">'):
            for key in key_mapping.keys():
                if key in text:
                    this_key = key_mapping[key]
        if '<td align="right">' in line:
            if this_key and not text.startswith('--'):
                # fix issue in table the ulgy way:
                text = text.replace('Windgeschwindigkeit: ', '')
                text = re.sub(r'[\(\)]', '', text)
                text = re.sub(r'\s+', ' ', text)
                data[this_key] = text.strip()
                this_key = None
        if line.startswith('<td colspan="2" align="center">'):
            text = ' '.join(':'.join(text.split(':')[1:]).strip().split(' ')[0:2])
            date = datetime.datetime.strptime(text, '%d.%m.%Y, %H:%M')
            data['date'] =  date
    return data


def parse_folder(folder='/opt/code/data/html/'):
    done_folder = Path('/opt/code/data/done')
    done_folder.mkdir(parents=True, exist_ok=True)
    for item in sorted(Path(folder).glob('*.htm')):
        data = None
        if 'statDE' in item.name:
            prefix = 'lubw'
            data = parse_lubw(item.open('rb').read())
        if 'Mitte--Schwabenzentrum' in item.name:
            prefix = 'stuttgart'
            data = parse_stadtklima_stgt(item.open('rb').read())
        if data:
            unix_timestamp = int(data['date'].timestamp())
            name = data['name'].replace(' ', '_')
            date = data['date'].date().isoformat()
            folder = Path('/opt/code/data/json') / Path(date)
            folder.mkdir(parents=True, exist_ok=True)
            fn_json = folder / f'{prefix}_{name}_{unix_timestamp}.json'
            with fn_json.open('w') as fp:
                data['date'] = data['date'].isoformat()
                json.dump(data, fp)
        item.rename(done_folder / item.name)


if __name__ == "__main__":
    parse_folder()
