import pytest
from cribbage_scorer import cribbage_scorer
import requests, json
import application as cs
import os
import tempfile


@pytest.fixture
def client():
    cs.application.config['TESTING'] = True
    return cs.application.test_client()


@pytest.mark.parametrize("request_data, correct_status_code", [
        ({"starter": [3,"C"], "dealer": "Abi"}, 400),
        ({"starter": ["Abi", "Bob"], "dealer": "Abi"}, 400),
        ({"players": ["Abi", "Bob"], "crib": [[3,"C"]]},400),
        ({"starter": -5}, 400),
        ({}, 400),        
        ([], 400)
])
def test_invalid_data_play_setclient(client, request_data, correct_status_code):

    resp = client.post("/score/show", json=request_data)

    assert resp.status_code == correct_status_code
