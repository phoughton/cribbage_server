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

@pytest.mark.parametrize("players, played_cards, correct_scorer_1, correct_score_1, correct_scorer_2, correct_score_2, correct_count", [
        (["Abi", "Bob"], [[3,"C"],[10,"D"],[10,"H"]], "Abi", 3, "Bob", 0, 23),
        (["Abi", "Bob"], [[11,"D"],[5, "D"]], "Abi", 0, "Bob", 3, 15),
        (["Abi", "Bob"], [[3,"C"],[10,"D"],[10,"H"],[8,"S"]], "Abi", 2, "Bob", 2, 31),
        (["Abi", "Bob"], [[3,"C"],[10,"D"],[10,"H"],[5,"S"],[3,"S"]], "Abi", 4, "Bob", 0, 31)
])
def test_play_whole_2_player(client, players, played_cards, correct_scorer_1, correct_score_1, correct_scorer_2, correct_score_2, correct_count):
    req_data = {
        "players": players,
        "played_cards": played_cards
    }
    resp = client.post("/score/play/set", json=req_data)
    resp_data = json.loads(resp.data)
    calc_scores = resp_data["score"]
    calc_play_log = resp_data["play_log"]

    assert calc_scores[correct_scorer_1] == correct_score_1, \
        f"The calculated score msg was: {calc_scores[correct_scorer_1] }, the expected score: {correct_score_1} " + \
        f"The play log {calc_play_log} "


@pytest.mark.parametrize("request_data, correct_status_code", [
        ({"cut_card": [3,"C"], "dealer": "Abi"}, 400),
        ({"players": ["Abi", "Bob"], "dealer": "Abi"}, 400),
        ({"players": ["Abi", "Bob"], "cut_card": [3,"C"]},400),
        ({"player": -5}, 400),
        ({}, 400),        
        ([], 400)
])
def test_invalid_data_play_set(client, request_data, correct_status_code):

    resp = client.post("/score/play/set", json=request_data)

    assert resp.status_code == correct_status_code


@pytest.mark.parametrize("played_cards, last_card, correct_score, correct_count", [
        ([[3,"C"],[10,"D"],[10,"H"]], False, 2, 23),
        ([[11,"D"],[5, "D"]], False, 2, 15),
        ([[11,"D"],[5, "D"]], True, 3, 15)
])
def test_play_ongoing_2_player(client, played_cards, last_card, correct_score, correct_count):
    req_data = {
        "last_card": last_card,
        "played_cards": played_cards
    }
    resp = client.post("/score/play/ongoing", json=req_data)
    resp_data = json.loads(resp.data)
    calc_count = resp_data["count"]
    calc_score = resp_data["score"]
    calc_play_log = resp_data["play_log"]

    assert calc_score == correct_score, \
        f"The calculated score msg was: {calc_score}, the expected score: {correct_score} " + \
        f"The play log {calc_play_log} "
    assert calc_count == correct_count, \
        f"The calculated count msg was: {calc_count}, the expected score: {correct_count} " + \
        f"The play log {calc_play_log} "
