import json
from typing import Optional

from flask import Blueprint, request

import left_leg_only_down
import left_leg_only_up
import right_leg_only_down_back
import right_leg_only_up
from apply_to_robot import apply_to_robot_nao


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


only_legs_up_api = Blueprint("only_legs_up_api", __name__, template_folder="templates")


@only_legs_up_api.route("/left_leg_only_down", methods=["GET"])
def left_leg_only_down_function():
    apply_to_robot_nao(left_leg_only_down)
    return application_json_response({
        "name": left_leg_only_down.names, 
        "keys": left_leg_only_down.keys,
        "times": left_leg_only_down.times
    }, 200)


@only_legs_up_api.route("/left_leg_only_up", methods=["GET"])
def left_leg_only_up_function():
    apply_to_robot_nao(left_leg_only_up)
    return application_json_response({
        "name": left_leg_only_up.names, 
        "keys": left_leg_only_up.keys,
        "times": left_leg_only_up.times
    }, 200)
    

@only_legs_up_api.route("/right_leg_only_down", methods=["GET"])
def right_leg_only_down_back_function():
    apply_to_robot_nao(right_leg_only_down_back)
    return application_json_response({
        "name": right_leg_only_down_back.names, 
        "keys": right_leg_only_down_back.keys,
        "times": right_leg_only_down_back.times
    }, 200)


@only_legs_up_api.route("/right_leg_only_up", methods=["GET"])
def right_leg_only_up_function():
    apply_to_robot_nao(right_leg_only_up)
    return application_json_response({
        "name": right_leg_only_up.names, 
        "keys": right_leg_only_up.keys,
        "times": right_leg_only_up.times
    }, 200)
 