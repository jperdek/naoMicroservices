import json
from flask import Blueprint, request


import lift_left_leg_on_chair1
import lift_right_leg_on_chair1
from apply_to_robot import apply_to_robot_nao


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


getting_up_from_chair_api = Blueprint("getting_up_from_chair_api", __name__, template_folder="templates")


@getting_up_from_chair_api.route("/lift_left_leg_on_chair", methods=["GET"])
def lift_left_leg_on_chair_function():
    apply_to_robot_nao(lift_left_leg_on_chair1)
    return application_json_response({
        "name": lift_left_leg_on_chair1.names,
        "keys": lift_left_leg_on_chair1.keys,
        "times": lift_left_leg_on_chair1.times
    }, 200)


@getting_up_from_chair_api.route("/lift_right_leg_on_chair", methods=["GET"])
def lift_right_leg_try_function():
    apply_to_robot_nao(lift_right_leg_on_chair1)
    return application_json_response({
        "name": lift_right_leg_on_chair1.names,
        "keys": lift_right_leg_on_chair1.keys,
        "times": lift_right_leg_on_chair1.times
    }, 200)
