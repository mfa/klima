import datetime
import requests
import time
from pathlib import Path
from tqdm import tqdm


def save_to_file(data, prefix, filename):
    unix_timestamp = int(time.time())
    fn = f'{prefix}_{unix_timestamp}_{filename}'
    with open(Path('/opt/code/data/html/') / Path(fn), 'w', encoding="latin-1") as fp:
        fp.write(data.decode('latin-1'))


def import_stuttgart():
    urls = ["http://www.stadtklima-stuttgart.de/index.php?luft_messdaten_station_smz"]

    for url in tqdm(urls, desc='stgt'):
        response = requests.get(url)
        assert response.status_code == 200
        save_to_file(response.content, 'stuttgart', 'Mitte--Schwabenzentrum.htm')


def import_lubw():
    base_url = "http://mnz.lubw.baden-wuerttemberg.de/messwerte/aktuell/"
    file_list = ["statDEBW004.htm", "statDEBW005.htm", "statDEBW006.htm",
                 "statDEBW009.htm", "statDEBW013.htm", "statDEBW015.htm",
                 "statDEBW019.htm", "statDEBW022.htm", "statDEBW023.htm",
                 "statDEBW024.htm", "statDEBW027.htm", "statDEBW029.htm",
                 "statDEBW031.htm", "statDEBW033.htm", "statDEBW038.htm",
                 "statDEBW039.htm", "statDEBW042.htm", "statDEBW046.htm",
                 "statDEBW052.htm", "statDEBW056.htm", "statDEBW059.htm",
                 "statDEBW073.htm", "statDEBW076.htm", "statDEBW080.htm",
                 "statDEBW081.htm", "statDEBW084.htm", "statDEBW087.htm",
                 "statDEBW098.htm", "statDEBW099.htm", "statDEBW107.htm",
                 "statDEBW112.htm", "statDEBW122.htm", "statDEBW125.htm",
                 "statDEBW147.htm", "statDEBW152.htm", "statDEBW156.htm", ]

    for filename in tqdm(file_list, desc='lubw'):
        response = requests.get(base_url + filename)
        assert response.status_code == 200
        save_to_file(response.content, 'lubw', filename)


if __name__ == "__main__":
    import_stuttgart()
    import_lubw()
