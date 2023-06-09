import pytest
from cribbage_scorer import cribbage_scorer
import requests, json
import app as cs
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


@pytest.mark.parametrize("request_data, correct_status_code, score", [
        ({"starter": [3,"C"], "crib": False, "hand": [(1,"H"), (2,"H"), (3,"H"), (4,"H")] }, 200, 14),
        ({"starter": [5,"C"], "crib": False, "hand": [(5,"H"), (5,"S"), (5,"D"), (11,"C")] }, 200, 29)

])
def test_valid_data_play_setclient(client, request_data, correct_status_code, score):

    resp = client.post("/score/show", json=request_data)

    assert resp.status_code == correct_status_code
    assert json.loads(resp.data)["score"] == score


@pytest.mark.parametrize("request_data, correct_status_code", [
        ({"starter": "KC", "hand": ["5H", "6D", "7S", "JC"],"isCrib": False}, 200),
        ({"starter": "AC", "hand": ["JH", "AS", "5H", "9C"], "isCrib": False}, 200)

])
def test_valid_data_simplified_show_score(client, request_data, correct_status_code):

    resp = client.post("/score_hand_show", json=request_data)

    assert resp.status_code == correct_status_code


@pytest.mark.parametrize("request_data, correct_status_code", [
        ({"starter": "KC", "hand": ["5H", "6D", "7S", "KC"],"isCrib": False}, 400),
        ({"starter": "9C", "hand": ["JH", "AS", "5H", "9C"], "isCrib": False}, 400),
        ({"starter": "2C", "hand": ["JH", "AS", "5H"], "isCrib": False}, 400)
])
def test_invalid_data_simplified_show_score(client, request_data, correct_status_code):

    resp = client.post("/score_hand_show", json=request_data)

    assert resp.status_code == correct_status_code