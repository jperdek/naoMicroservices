import json
from typing import Optional

from flask import Blueprint, request

import forearm_raising_left_leg
import forearm_raising_right_leg
import put_hands_to_body_forearm_raised_left_leg_back
import put_hands_to_body_forearm_raised_right_leg_back
from apply_to_robot import apply_to_robot_nao


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


forearm_in_sitting_leg_api = Blueprint("forearm_in_sitting_leg_api", __name__, template_folder="templates")


@forearm_in_sitting_leg_api.route("/forearm_raising_left_leg", methods=["GET"])
def forearm_raising_left_leg_function():
    apply_to_robot_nao(forearm_raising_left_leg)
    return application_json_response({
        "name": forearm_raising_left_leg.names,
        "keys": forearm_raising_left_leg.keys,
        "times": forearm_raising_left_leg.times
    }, 200)
    

@forearm_in_sitting_leg_api.route("/forearm_raising_right_leg", methods=["GET"])
def forearm_raising_right_leg_function():
    apply_to_robot_nao(forearm_raising_right_leg)
    return application_json_response({
        "name": forearm_raising_right_leg.names, 
        "keys": forearm_raising_right_leg.keys,
        "times": forearm_raising_right_leg.times
    }, 200)
    
 
@forearm_in_sitting_leg_api.route("/put_hands_to_body_forearm_raised_left_leg_back", methods=["GET"])
def put_hands_to_body_forearm_raised_left_leg_back_function():
    apply_to_robot_nao(put_hands_to_body_forearm_raised_left_leg_back)
    return application_json_response({
        "name": put_hands_to_body_forearm_raised_left_leg_back.names, 
        "keys": put_hands_to_body_forearm_raised_left_leg_back.keys,
        "times": put_hands_to_body_forearm_raised_left_leg_back.times
    }, 200)


@forearm_in_sitting_leg_api.route("/put_hands_to_body_forearm_raised_right_leg_back", methods=["GET"])
def put_hands_to_body_forearm_raised_right_leg_back_function():
    apply_to_robot_nao(put_hands_to_body_forearm_raised_right_leg_back)
    return application_json_response({
        "name": put_hands_to_body_forearm_raised_right_leg_back.names,
        "keys": put_hands_to_body_forearm_raised_right_leg_back.keys,
        "times": put_hands_to_body_forearm_raised_right_leg_back.times
    }, 200)
