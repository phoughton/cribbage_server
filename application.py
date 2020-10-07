from flask import Flask, abort, request, jsonify
import errors

from cribbage_scorer import cribbage_scorer as cs

application = Flask(__name__)


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

    calc_scores, msg  = cs.cut_calc_score(cut_card, players, dealer)

    return {"score": calc_scores, "message": msg}


@application.route("/score/play", methods=["GET", "POST"])
def playcalcscore():
    pass


@application.route("/score/show", methods=["GET", "POST"])
def showcalcscore():
    pass


