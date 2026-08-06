import json

from flask import Blueprint

import hands_in_sitting_up
import hands_in_sitting_down
import hands_in_standing_down
import hands_in_standing_up
import hands_in_standing_up2
from apply_to_robot import apply_to_robot_nao


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


arm_circling_in_standing_api = Blueprint("arm_circling_in_standing_api", __name__, template_folder="templates")


@arm_circling_in_standing_api.route("/hands_in_sitting_up", methods=["GET"])
def hands_in_sitting_up_function():
    apply_to_robot_nao(hands_in_sitting_up)
    return application_json_response({
        "name": hands_in_sitting_up.names, 
        "keys": hands_in_sitting_up.keys,
        "times": hands_in_sitting_up.times
    }, 200)
    

@arm_circling_in_standing_api.route("/hands_in_sitting_down", methods=["GET"])
def hands_in_sitting_down_function():
    apply_to_robot_nao(hands_in_sitting_down)
    return application_json_response({
        "name": hands_in_sitting_down.names, 
        "keys": hands_in_sitting_down.keys,
        "times": hands_in_sitting_down.times
    }, 200)


@arm_circling_in_standing_api.route("/hands_in_standing_down", methods=["GET"])
def hands_in_standing_down_function():
    apply_to_robot_nao(hands_in_standing_down)
    return application_json_response({
        "name": hands_in_standing_down.names, 
        "keys": hands_in_standing_down.keys,
        "times": hands_in_standing_down.times
    }, 200)
    

@arm_circling_in_standing_api.route("/hands_in_standing_up", methods=["GET"])
def hands_in_standing_up_function():
    apply_to_robot_nao(hands_in_standing_up)
    return application_json_response({
        "name": hands_in_standing_up.names, 
        "keys": hands_in_standing_up.keys,
        "times": hands_in_standing_up.times
    }, 200)


@arm_circling_in_standing_api.route("/hands_in_standing_up2", methods=["GET"])
def hands_in_standing_up2_function():
    apply_to_robot_nao(hands_in_standing_up2)
    return application_json_response({
        "name": hands_in_standing_up2.names, 
        "keys": hands_in_standing_up2.keys,
        "times": hands_in_standing_up2.times
    }, 200)

    
