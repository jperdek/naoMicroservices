import json
from flask import Blueprint, request

import return_hands_from_t_pose_in_sitting
import return_legs_from_t_pose_in_sitting_back
import return_legs_from_t_pose_in_sitting_without_hands_back
from apply_to_robot import apply_to_robot_nao


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


return_to_pose_in_sitting_api = Blueprint("return_to_pose_in_sitting_api", __name__, template_folder="templates")


@return_to_pose_in_sitting_api.route("/return_hands_from_t_pose_in_sitting", methods=["GET"])
def return_hands_from_t_pose_in_sitting_function():
    apply_to_robot_nao(return_hands_from_t_pose_in_sitting)
    return application_json_response({
        "name": return_hands_from_t_pose_in_sitting.names, 
        "keys": return_hands_from_t_pose_in_sitting.keys,
        "times": return_hands_from_t_pose_in_sitting.times
    }, 200)
    

@return_to_pose_in_sitting_api.route("/return_legs_from_t_pose_in_sitting_back", methods=["GET"])
def return_legs_from_t_pose_in_sitting_back_function():
    apply_to_robot_nao(return_legs_from_t_pose_in_sitting_back)
    return application_json_response({
        "name": return_legs_from_t_pose_in_sitting_back.names, 
        "keys": return_legs_from_t_pose_in_sitting_back.keys,
        "times": return_legs_from_t_pose_in_sitting_back.times
    }, 200)
    
 
@return_to_pose_in_sitting_api.route("/return_legs_from_t_pose_in_sitting_without_hands_back", methods=["GET"])
def return_legs_from_t_pose_in_sitting_without_hands_back_function():
    apply_to_robot_nao(return_legs_from_t_pose_in_sitting_without_hands_back)
    return application_json_response({
        "name": return_legs_from_t_pose_in_sitting_without_hands_back.names, 
        "keys": return_legs_from_t_pose_in_sitting_without_hands_back.keys,
        "times": return_legs_from_t_pose_in_sitting_without_hands_back.times
    }, 200)

