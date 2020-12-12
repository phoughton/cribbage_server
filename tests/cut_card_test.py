import pytest
from cribbage_scorer import cribbage_scorer
import requests, json
from cribbage_server import application as cs
import os
import tempfile


@pytest.fixture
def client():
    cs.application.config['TESTING'] = True
    return cs.application.test_client()

@pytest.mark.parametrize("players, cut_card, dealer, expected_score, expected_scorer", [
        (["Abi", "Bob"], [3,"C"], "Abi", 0, None),
        (["Abi", "Bob"], [11,"D"], "Abi", 2, "Abi")
])
def test_simple_hands1(client, players, cut_card, dealer, expected_score, expected_scorer):
    req_data = {
        "players": players,
        "cut_card": cut_card,
        "dealer": dealer
    }
    resp = client.post("/score/cut", json=req_data)
    resp_data = json.loads(resp.data)
    calc_score = resp_data["score"]
    calc_msg = resp_data["message"]

    if expected_scorer is None:
        for each_score in calc_score.values():
            assert each_score == 0, f"The calculated score msg was: {calc_score}, should be 0"

    else:
        assert calc_score[expected_scorer] == expected_score, \
            f"The calculated score msg was: {calc_score}, the expected score: {expected_score}, and expected scorer was: {expected_scorer}. " + \
            f"The hand description was: {calc_msg} "
