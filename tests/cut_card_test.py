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

@pytest.mark.parametrize("players, cut_card, dealer, correct_score, correct_scorer", [
        (["Abi", "Bob"], [3,"C"], "Abi", 0, None),
        (["Abi", "Bob"], [11,"D"], "Abi", 2, "Abi")
])
def test_simple_hands1(client, players, cut_card, dealer, correct_score, correct_scorer):
    req_data = {
        "players": players,
        "cut_card": cut_card,
        "dealer": dealer
    }
    resp = client.post("/score/cut", json=req_data)
    resp_data = json.loads(resp.data)
    calc_score = resp_data["score"]
    calc_msg = resp_data["message"]

    if correct_scorer is None:
        for each_score in calc_score.values():
            assert each_score == 0, f"The calculated score msg was: {calc_score}, should be 0"

    else:
        assert calc_score[correct_scorer] == correct_score, \
            f"The calculated score msg was: {calc_score}, the expected score: {correct_score}, and expected scorer was: {correct_scorer}. " + \
            f"The hand description was: {calc_msg} "


@pytest.mark.parametrize("request_data, correct_status_code", [
        ({"cut_card": [3,"C"], "dealer": "Abi"}, 400),
        ({"players": ["Abi", "Bob"], "dealer": "Abi"}, 400),
        ({"players": ["Abi", "Bob"], "cut_card": [3,"C"]},400),
        ({"player": -5}, 400),
        ({}, 400),        
        ([], 400)
])
def test_invalid_data(client, request_data, correct_status_code):

    resp = client.post("/score/cut", json=request_data)

    assert resp.status_code == correct_status_code

