from flask import Flask, request, jsonify, abort, render_template, send_from_directory
import errors
from functools import wraps
from cribbage_scorer import cribbage_scorer as cs
from datetime import datetime
from flask_cors import CORS
from flask import Response


application = Flask(__name__)
CORS(application)
MAX_DATA_LIMIT = 10*1024

@application.route("/")
def webapp():
    return render_template('index.html')

@application.route("/.well-known/ai-plugin.json")
def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
    
    return text

@application.route("/openapi.yaml")
def openapi():
    with open("./openapi.yaml") as f:
        text = f.read()
    
    return Response(text, mimetype="text/yaml")

@application.route("/legal")
def legal():
    return render_template('legal.html')


@application.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('templates/js', path)


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


@application.route("/health", methods=["GET"])
def health_check():

    return { "status": "UP", "current_time" : f"{datetime.now().astimezone().isoformat()}"}


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

    scores, current_count, play_log = cs.play_calc_score_set(played_cards, players)

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

    current_count, scores, play_log = cs.play_score_ongoing(played_cards, last_card)

    return {"type": "play", "score": scores, "count": current_count, "play_log": play_log}


@application.route("/score/show", methods=["POST"])
def showcalcscore():

    req_data = request.get_json()
    errors.check_for_required_fields(req_data, ["starter", "hand", "crib"])

    starter = tuple(req_data["starter"])
    hand = lists_to_tuples(req_data["hand"])
    crib = req_data["crib"]

    score, msg = cs.show_calc_score(starter, hand, crib)

    return {"type": "show", "score": score, "message": msg}


@application.route("/score_hand_show", methods=["POST"])
def show_calc_score_open_api():

    ranks_to_num = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5,
                    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                    "J": 11, "Q": 12, "K": 13}

    req_data = request.get_json()
    errors.check_for_required_fields(req_data, ["starter", "hand", "isCrib"])
    errors.check_for_fields_populated(req_data, "hand", 4)

    hand = []
    for card in req_data["hand"]:
        if len(card) > 3:
            raise Exception("Error: Invalid card ID.")
        suit = card[-1]
        
        if len(card) == 3:
            rank = card[0:2]
        else:
            rank = card[0]
        hand.append((ranks_to_num.get(rank), suit))
    
    if len(req_data["starter"]) == 3:
        starter = (ranks_to_num.get(req_data["starter"][0:2]), req_data["starter"][-1])
    else:
        starter = (ranks_to_num.get(req_data["starter"][0]), req_data["starter"][-1])

    crib = req_data["isCrib"]

    score, msg = cs.show_calc_score(starter, hand, crib)

    return {"type": "show", "score": score, "message": msg}


if __name__ == "__main__":
    application.run(port=5000, host="0.0.0.0")
    