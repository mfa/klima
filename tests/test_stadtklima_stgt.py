import pytest
from pathlib import Path

from klima.parsers import parse_stadtklima_stgt


@pytest.fixture
def stadtklima_stgt_fixture():
    with open(Path(__file__).parent / Path('fixtures/stadtklima_stuttgart.html'), 'rb') as fp:
        yield fp.read()

def test_lubw(stadtklima_stgt_fixture):
    result = parse_stadtklima_stgt(stadtklima_stgt_fixture)
    assert len(result) == 5
    assert result[0]['name'] == 'Eggenstein'
    assert result[0]['component'] == 'Feinstaub (PM10)'
    assert result[-1]['maximum_value'] == '17'
