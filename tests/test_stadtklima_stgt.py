import datetime
import pytest
from pathlib import Path

from klima.parsers import parse_stadtklima_stgt


@pytest.fixture
def stadtklima_stgt_fixture():
    with open(Path(__file__).parent / Path('fixtures/stadtklima_stuttgart.html'), 'rb') as fp:
        yield fp.read()

def test_stadtklima(stadtklima_stgt_fixture):
    result = parse_stadtklima_stgt(stadtklima_stgt_fixture)
    assert len(result) == 18
    assert result['date'] == datetime.datetime(2018, 9, 20, 20, 30)
    assert result['name'] == 'Mitte--Schwabenzentrum'
    assert result['temperature'] == '25.9 °C'
    assert result['wind speed'] == '0.3 m/s, 1.1 km/h'
    assert 'PM2.5' not in result
