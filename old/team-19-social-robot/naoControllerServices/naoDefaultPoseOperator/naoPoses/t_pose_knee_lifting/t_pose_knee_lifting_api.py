import json
from typing import Optional

from flask import Blueprint, request

import return_hands_from_t_pose_back
import return_hands_from_base_posture
import t_pose_lifting_left_knee
import t_pose_lifting_right_knee
import return_hands_from_t_pose_raised_left_knee
from apply_to_robot import apply_to_robot_nao


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


t_pose_knee_lifting_api = Blueprint("t_pose_knee_lifting_api", __name__, template_folder="templates")


@t_pose_knee_lifting_api.route("/return_hands_from_t_pose_back", methods=["GET"])
def return_hands_from_t_pose_back_function():
    apply_to_robot_nao(return_hands_from_t_pose_back)
    return application_json_response({
        "name": return_hands_from_t_pose_back.names,
        "keys": return_hands_from_t_pose_back.keys,
        "times": return_hands_from_t_pose_back.times
    }, 200)


@t_pose_knee_lifting_api.route("/return_hands_from_base_posture", methods=["GET"])
def return_hands_from_base_posture_function():
    apply_to_robot_nao(return_hands_from_base_posture)
    return application_json_response({
        "name": return_hands_from_base_posture.names,
        "keys": return_hands_from_base_posture.keys,
        "times": return_hands_from_base_posture.times
    }, 200)


@t_pose_knee_lifting_api.route("/t_pose_lifting_left_knee", methods=["GET"])
def t_pose_lifting_left_knee_function():
    apply_to_robot_nao(t_pose_lifting_left_knee)
    return application_json_response({
        "name": t_pose_lifting_left_knee.names,
        "keys": t_pose_lifting_left_knee.keys,
        "times": t_pose_lifting_left_knee.times
    }, 200)


@t_pose_knee_lifting_api.route("/t_pose_lifting_right_knee", methods=["GET"])
def t_pose_lifting_right_knee_function():
    apply_to_robot_nao(t_pose_lifting_right_knee)
    return application_json_response({
        "name": t_pose_lifting_right_knee.names,
        "keys": t_pose_lifting_right_knee.keys,
        "times": t_pose_lifting_right_knee.times
    }, 200)


@t_pose_knee_lifting_api.route("/return_hands_from_t_pose_raised_left_knee", methods=["GET"])
def return_hands_from_t_pose_raised_left_knee_function():
    apply_to_robot_nao(return_hands_from_t_pose_raised_left_knee)
    return application_json_response({
        "name": return_hands_from_t_pose_raised_left_knee.names,
        "keys": return_hands_from_t_pose_raised_left_knee.keys,
        "times": return_hands_from_t_pose_raised_left_knee.times
    }, 200)

