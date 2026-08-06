import json
from typing import Optional

from flask import Blueprint, request

import changed_foot_in_lying
import right_foot_put_in_base_lying_pose
import straighten_hands_in_lying
from apply_to_robot import apply_to_robot_nao


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


other_in_lying_api = Blueprint("other_in_lying_api", __name__, template_folder="templates")


@other_in_lying_api.route("/changed_foot_in_lying", methods=["GET"])
def changed_foot_in_lying_function():
    apply_to_robot_nao(changed_foot_in_lying)
    return application_json_response({
        "name": changed_foot_in_lying.names, 
        "keys": changed_foot_in_lying.keys,
        "times": changed_foot_in_lying.times
    }, 200)


@other_in_lying_api.route("/right_foot_put_in_base_lying_pose", methods=["GET"])
def right_foot_put_in_base_lying_pose_function():
    apply_to_robot_nao(right_foot_put_in_base_lying_pose)
    return application_json_response({
        "name": right_foot_put_in_base_lying_pose.names, 
        "keys": right_foot_put_in_base_lying_pose.keys,
        "times": right_foot_put_in_base_lying_pose.times
    }, 200)
    

@other_in_lying_api.route("/straighten_hands_in_lying", methods=["GET"])
def straighten_hands_in_lying_function():
    apply_to_robot_nao(straighten_hands_in_lying)
    return application_json_response({
        "name": straighten_hands_in_lying.names, 
        "keys": straighten_hands_in_lying.keys,
        "times": straighten_hands_in_lying.times
    }, 200)
