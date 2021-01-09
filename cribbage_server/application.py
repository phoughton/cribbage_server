from flask import Flask, request, jsonify, abort
from cribbage_server import errors
from functools import wraps
from cribbage_scorer import cribbage_scorer as cs

application = Flask(__name__)
MAX_DATA_LIMIT = 10*1024


def lists_to_tuples(list_of_lists):
    out_list = []
    for a_list in list_of_lists:
        if len(a_list) > 2:
            raise Exception("Error: Card ID list can not be converted to tuple as too many members.")
        out_list.append(tuple(a_list))
    return out_list


def limit_content_length(max_length=MAX_DATA_LIMIT):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            if cl is not None and cl > max_length:
                abort(413)
            return f(*args, **kwargs)
        return wrapper
    return decorator

@application.errorhandler(errors.InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@application.route("/score/cut", methods=["POST"])
@limit_content_length()
def cutcalcscore():
    required_fields = ["players", "cut_card", "dealer"]
    
    try:
        req_data = request.get_json()
    except:
        errors.check_for_required_fields(None,required_fields)

    errors.check_for_required_fields(req_data,required_fields)

    players = req_data["players"]
    cut_card = tuple(req_data["cut_card"])
    dealer = req_data["dealer"]

    scores, msg = cs.cut_calc_score(cut_card, players, dealer)

    return {"type": "cut", "score": scores, "message": msg}


@application.route("/score/play/set", methods=["POST"])
def playcalcscorewhole():

    req_data = request.get_json()
    errors.check_for_required_fields(req_data, ["players", "played_cards"])

    players = req_data["players"]
    played_cards = lists_to_tuples(req_data["played_cards"])

    scores, current_count, play_log = cs.play_calc_score_whole_game(played_cards, players)

    return {"type": "playwhole", "score": scores, "current_count": current_count, "play_log": play_log}


@application.route("/score/play/ongoing", methods=["POST"])
def playcalcscore():

    req_data = request.get_json()
    errors.check_for_required_fields(req_data, ["played_cards"])

    played_cards = lists_to_tuples(req_data["played_cards"])
    if "last_card" in req_data:
        last_card = req_data["last_card"]
    else:
        last_card = False

    current_count, scores, play_log = cs.play_score_just_made(played_cards, last_card)

    return {"type": "play", "score": scores, "count": current_count, "play_log": play_log}


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
