import json
import pytest

from trustar2 import Account, TruStar
from tests.unit.resources import ENCLAVES


URL = "https://api.trustar.co/api/2.0"


@pytest.fixture
def account(ts):
    return Account(ts)


@pytest.fixture
def enclaves_response():
    return json.loads(ENCLAVES)


def test_ping_successfully(account, mocked_request):
    mocked_request.get(URL + "/ping", status_code=200, text="pong\n")
    response = account.ping()
    assert response.status_code == 200
    assert response.data.get("result") == "pong\n"


def test_get_enclaves_successfully(account, mocked_request, enclaves_response):
    mocked_request.get(URL + "/enclaves", json=enclaves_response)
    response = account.get_enclaves()
    current_enclaves = [e.serialize() for e in response.data]
    assert response.status_code == 200
    assert current_enclaves == enclaves_response
    assert len(current_enclaves) == len(enclaves_response)
