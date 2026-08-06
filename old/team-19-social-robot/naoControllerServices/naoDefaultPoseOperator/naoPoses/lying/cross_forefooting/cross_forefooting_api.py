import json
from typing import Optional

from flask import Blueprint, request

import left_leg_right_hand_down_back
import left_leg_right_hand_up
import right_leg_left_hand_down_back
import right_leg_left_hand_up
from apply_to_robot import apply_to_robot_nao


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


cross_forefooting_api = Blueprint("cross_forefooting_api", __name__, template_folder="templates")


@cross_forefooting_api.route("/left_leg_right_hand_up", methods=["GET"])
def left_leg_right_hand_up_function():
    apply_to_robot_nao(left_leg_right_hand_up)
    return application_json_response({
        "name": left_leg_right_hand_up.names, 
        "keys": left_leg_right_hand_up.keys,
        "times": left_leg_right_hand_up.times
    }, 200)


@cross_forefooting_api.route("/left_leg_right_hand_down_back", methods=["GET"])
def left_leg_right_hand_down_back_function():
    apply_to_robot_nao(left_leg_right_hand_down_back)
    return application_json_response({
        "name": left_leg_right_hand_down_back.names, 
        "keys": left_leg_right_hand_down_back.keys,
        "times": left_leg_right_hand_down_back.times
    }, 200)
    
    
@cross_forefooting_api.route("/right_leg_left_hand_up", methods=["GET"])
def right_leg_left_hand_up_function():
    apply_to_robot_nao(right_leg_left_hand_up)
    return application_json_response({
        "name": right_leg_left_hand_up.names, 
        "keys": right_leg_left_hand_up.keys,
        "times": right_leg_left_hand_up.times
    }, 200)
    

@cross_forefooting_api.route("/right_leg_left_hand_down_back", methods=["GET"])
def right_leg_left_hand_down_back_function():
    apply_to_robot_nao(right_leg_left_hand_down_back)
    return application_json_response({
        "name": right_leg_left_hand_down_back.names, 
        "keys": right_leg_left_hand_down_back.keys,
        "times": right_leg_left_hand_down_back.times
    }, 200)


