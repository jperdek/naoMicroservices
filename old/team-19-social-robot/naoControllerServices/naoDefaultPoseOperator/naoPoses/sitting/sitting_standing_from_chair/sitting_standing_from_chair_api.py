import json
from typing import Optional

from flask import Blueprint, request

import sit_excercise
import sitting_in_chair_fast
import stand_up_from_chair
import stand_up_from_chair_fast
from apply_to_robot import apply_to_robot_nao


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


sitting_standing_from_chair_api = Blueprint("sitting_standing_from_chair_api", __name__, template_folder="templates")


@sitting_standing_from_chair_api.route("/sit_excercise", methods=["GET"])
def sit_excercise_function():
    apply_to_robot_nao(sit_excercise)
    return application_json_response({
        "name": sit_excercise.names, 
        "keys": sit_excercise.keys,
        "times": sit_excercise.times
    }, 200)
    

@sitting_standing_from_chair_api.route("/sitting_in_chair_fast", methods=["GET"])
def sitting_in_chair_fast_function():
    apply_to_robot_nao(sitting_in_chair_fast)
    return application_json_response({
        "name": sitting_in_chair_fast.names, 
        "keys": sitting_in_chair_fast.keys,
        "times": sitting_in_chair_fast.times
    }, 200)


@sitting_standing_from_chair_api.route("/stand_up_from_chair", methods=["GET"])
def stand_up_from_chair_function():
    apply_to_robot_nao(stand_up_from_chair)
    return application_json_response({
        "name": stand_up_from_chair.names, 
        "keys": stand_up_from_chair.keys,
        "times": stand_up_from_chair.times
    }, 200)
    

@sitting_standing_from_chair_api.route("/stand_up_from_chair_fast", methods=["GET"])
def stand_up_from_chair_fast_function():
    apply_to_robot_nao(stand_up_from_chair_fast)
    return application_json_response({
        "name": stand_up_from_chair_fast.names, 
        "keys": stand_up_from_chair_fast.keys,
        "times": stand_up_from_chair_fast.times
    }, 200)
 