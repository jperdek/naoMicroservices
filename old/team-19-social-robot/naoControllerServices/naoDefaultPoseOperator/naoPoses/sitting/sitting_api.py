import json
from typing import Optional

from flask import Blueprint, request

import lower_arms_from_sitting_position
import sitting_position_for_extending_legs
from apply_to_robot import apply_to_robot_nao


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


sitting_api = Blueprint("sitting_api", __name__, template_folder="templates")


@sitting_api.route("/lower_arms_from_sitting_position", methods=["GET"])
def lower_arms_from_sitting_position_function():
    apply_to_robot_nao(lower_arms_from_sitting_position)
    return application_json_response({
        "name": lower_arms_from_sitting_position.names, 
        "keys": lower_arms_from_sitting_position.keys,
        "times": lower_arms_from_sitting_position.times
    }, 200)
    

@sitting_api.route("/sitting_position_for_extending_legs", methods=["GET"])
def sitting_position_for_extending_legs_function():
    apply_to_robot_nao(sitting_position_for_extending_legs)
    return application_json_response({
        "name": sitting_position_for_extending_legs.names, 
        "keys": sitting_position_for_extending_legs.keys,
        "times": sitting_position_for_extending_legs.times
    }, 200)
 
