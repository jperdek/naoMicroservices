import json
from typing import Optional

from flask import Blueprint, request

import forearm_raising_left_knee
import forearm_raising_right_knee
import put_hands_to_body_forearm_raised_left_knee_back
import put_hands_to_body_forearm_raised_right_knee_back
from apply_to_robot import apply_to_robot_nao


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


forearm_in_sitting_knee_api = Blueprint("forearm_in_sitting_knee_api", __name__, template_folder="templates")


@forearm_in_sitting_knee_api.route("/forearm_raising_left_knee", methods=["GET"])
def forearm_raising_left_knee_function():
    apply_to_robot_nao(forearm_raising_left_knee)
    return application_json_response({
        "name": forearm_raising_left_knee.names, 
        "keys": forearm_raising_left_knee.keys,
        "times": forearm_raising_left_knee.times
    }, 200)
    

@forearm_in_sitting_knee_api.route("/forearm_raising_right_knee", methods=["GET"])
def forearm_raising_right_knee_function():
    apply_to_robot_nao(forearm_raising_right_knee)
    return application_json_response({
        "name": forearm_raising_right_knee.names, 
        "keys": forearm_raising_right_knee.keys,
        "times": forearm_raising_right_knee.times
    }, 200)
    
 
@forearm_in_sitting_knee_api.route("/put_hands_to_body_forearm_raised_left_knee_back", methods=["GET"])
def put_hands_to_body_forearm_raised_left_knee_back_function():
    apply_to_robot_nao(put_hands_to_body_forearm_raised_left_knee_back)
    return application_json_response({
        "name": put_hands_to_body_forearm_raised_left_knee_back.names, 
        "keys": put_hands_to_body_forearm_raised_left_knee_back.keys,
        "times": put_hands_to_body_forearm_raised_left_knee_back.times
    }, 200)
    

@forearm_in_sitting_knee_api.route("/put_hands_to_body_forearm_raised_right_knee_back", methods=["GET"])
def put_hands_to_body_forearm_raised_right_knee_back_function():
    apply_to_robot_nao(put_hands_to_body_forearm_raised_right_knee_back)
    return application_json_response({
        "name": put_hands_to_body_forearm_raised_right_knee_back.names, 
        "keys": put_hands_to_body_forearm_raised_right_knee_back.keys,
        "times": put_hands_to_body_forearm_raised_right_knee_back.times
    }, 200)

 