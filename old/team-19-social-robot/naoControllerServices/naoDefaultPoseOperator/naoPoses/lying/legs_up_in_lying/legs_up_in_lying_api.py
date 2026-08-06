import json
from typing import Optional

from flask import Blueprint, request

import left_foot_in_lying_back
import lift_right_foot_in_lying_back
import legs_up_in_lying_api
from apply_to_robot import apply_to_robot_nao


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


legs_up_in_lying_api = Blueprint("legs_up_in_lying_api", __name__, template_folder="templates")


@legs_up_in_lying_api.route("/legs_up_in_lying", methods=["GET"])
def legs_up_in_lying():
    apply_to_robot_nao(legs_up_in_lying)
    return application_json_response({
        "name": legs_up_in_lying.names, 
        "keys": legs_up_in_lying.keys,
        "times": legs_up_in_lying.times
    }, 200)


@legs_up_in_lying_api.route("/left_foot_in_lying_back", methods=["GET"])
def left_foot_in_lying_back():
    apply_to_robot_nao(left_foot_in_lying_back)
    return application_json_response({
        "name": left_foot_in_lying_back.names, 
        "keys": left_foot_in_lying_back.keys,
        "times": left_foot_in_lying_back.times
    }, 200)
    
    
@legs_up_in_lying_api.route("/lift_right_foot_in_lying_back", methods=["GET"])
def lift_right_foot_in_lying_back():
    apply_to_robot_nao(lift_right_foot_in_lying_back)
    return application_json_response({
        "name": lift_right_foot_in_lying_back.names, 
        "keys": lift_right_foot_in_lying_back.keys,
        "times": lift_right_foot_in_lying_back.times
    }, 200)
