import pytest
from pathlib import Path

from klima.parsers import parse_lubw


@pytest.fixture
def lubw_fixture():
    with open(Path(__file__).parent / Path('fixtures/lubw.html'), 'rb') as fp:
        yield fp.read()

def test_lubw(lubw_fixture):
    result = parse_lubw(lubw_fixture)
    assert len(result) == 3
    assert len(result['items']) == 5
    assert result['name'] == 'Eggenstein'
    assert result['items'][0]['component'] == 'Feinstaub (PM10)'
    assert result['items'][-1]['maximum_value'] == '17'
