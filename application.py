from flask import Flask, request, jsonify
import errors

from cribbage_scorer import cribbage_scorer as cs

application = Flask(__name__)


def lists_to_tuples(list_of_lists):
    out_list = []
    for a_list in list_of_lists:
        if len(a_list) > 2:
            raise Exception("Error: Card ID list can not be converted to tuple as too many members.")
        out_list.append(tuple(a_list))
    return out_list


@application.errorhandler(errors.InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@application.route("/score/cut", methods=["POST"])
def cutcalcscore():

    req_data = request.get_json()
    errors.check_for_required_fields(req_data, ["players", "cut_card", "dealer"])

    players = req_data["players"]
    cut_card = tuple(req_data["cut_card"])
    dealer = req_data["dealer"]

    scores, msg = cs.cut_calc_score(cut_card, players, dealer)

    return {"type": "cut", "score": scores, "message": msg}


@application.route("/score/play", methods=["POST"])
def playcalcscore():

    req_data = request.get_json()
    errors.check_for_required_fields(req_data, ["players", "played_cards"])

    players = req_data["players"]
    played_cards = lists_to_tuples(req_data["played_cards"])

    scores, current_count, play_log = cs.play_calc_score_whole_game(played_cards, players)

    return {"type": "play", "score": scores, "current_count": current_count, "play_log": play_log}


@application.route("/score/show", methods=["POST"])
def showcalcscore():

    req_data = request.get_json()
    errors.check_for_required_fields(req_data, ["starter", "hand", "crib"])

    starter = tuple(req_data["starter"])
    hand = lists_to_tuples(req_data["hand"])
    crib = req_data["crib"]

    print(starter, hand, crib)
    score, msg = cs.show_calc_score(starter, hand, crib)

    return {"type": "show", "score": score, "message": msg}
