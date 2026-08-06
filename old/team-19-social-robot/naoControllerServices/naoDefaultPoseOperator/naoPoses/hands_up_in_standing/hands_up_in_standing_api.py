import json
from typing import Optional

from flask import Blueprint, request

import hands_down_left_leg_back
import hands_down_right_leg_back
import hands_up_lifting_left_leg
import hands_up_lifting_right_leg
from apply_to_robot import apply_to_robot_nao


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


hands_up_in_standing_api = Blueprint("hands_up_in_standing_api", __name__, template_folder="templates")


@hands_up_in_standing_api.route("/hands_down_left_leg_back", methods=["GET"])
def hands_down_left_leg_back_function():
    apply_to_robot_nao(hands_down_left_leg_back)
    return application_json_response({
        "name": hands_down_left_leg_back.names, 
        "keys": hands_down_left_leg_back.keys,
        "times": hands_down_left_leg_back.times
    }, 200)


@hands_up_in_standing_api.route("/hands_down_right_leg_back", methods=["GET"])
def hands_down_right_leg_back_function():
    apply_to_robot_nao(hands_down_right_leg_back)
    return application_json_response({
        "name": hands_down_right_leg_back.names, 
        "keys": hands_down_right_leg_back.keys,
        "times": hands_down_right_leg_back.times
    }, 200)
    

@hands_up_in_standing_api.route("/hands_up_lifting_left_leg", methods=["GET"])
def hands_up_lifting_left_leg_function():
    apply_to_robot_nao(hands_up_lifting_left_leg)
    return application_json_response({
        "name": hands_up_lifting_left_leg.names, 
        "keys": hands_up_lifting_left_leg.keys,
        "times": hands_up_lifting_left_leg.times
    }, 200)


@hands_up_in_standing_api.route("/hands_up_lifting_right_leg", methods=["GET"])
def hands_up_lifting_right_leg_function():
    apply_to_robot_nao(hands_up_lifting_right_leg)
    return application_json_response({
        "name": hands_up_lifting_right_leg.names, 
        "keys": hands_up_lifting_right_leg.keys,
        "times": hands_up_lifting_right_leg.times
    }, 200)
    
