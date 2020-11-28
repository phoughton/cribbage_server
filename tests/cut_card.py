import pytest
from cribbage_scorer import cribbage_scorer
import requests, json

host="localhost"
port="5000"
url=f"http://{host}:{port}"

@pytest.mark.parametrize("players, cut_card, dealer, expected_score, expected_scorer", [
        (["Abi", "Bob"], [3,"C"], "Abi", 0, None),
        (["Abi", "Bob"], [11,"D"], "Abi", 2, "Abi")
])
def test_simple_hands1(players, cut_card, dealer, expected_score, expected_scorer):
    req_data = {
        "players": players,
        "cut_card": cut_card,
        "dealer": dealer
    }
    resp = requests.post(url+"/score/cut", json=req_data)
    resp_data = json.loads(resp.text)
    calc_score = resp_data["score"]
    calc_msg = resp_data["message"]


    print(calc_score, calc_msg)
    if expected_scorer is not None:
        assert calc_score[expected_scorer] == expected_score, \
            f"The calculated score msg was: {calc_score}, the expected score: {expected_score}, and expected scorer was: {expected_scorer}. " + \
            f"The hand description was: {calc_msg} "
        # incomplete
    # add else
