import json
from typing import Optional

from flask import Blueprint, request

import lift_hands_up_in_lying
import put_hands_to_body_in_lying_back


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


only_hands_up_in_lying_api = Blueprint("only_hands_up_in_lying_api", __name__, template_folder="templates")


@only_hands_up_in_lying_api.route("/lift_hands_up_in_lying", methods=["GET"])
def lift_hands_up_in_lying():
    return application_json_response({
        "name": lift_hands_up_in_lying.names, 
        "keys": lift_hands_up_in_lying.keys,
        "times": lift_hands_up_in_lying.times
    }, 200)


@only_hands_up_in_lying_api.route("/put_hands_to_body_in_lying_back", methods=["GET"])
def put_hands_to_body_in_lying_back():
    return application_json_response({
        "name": put_hands_to_body_in_lying_back.names, 
        "keys": put_hands_to_body_in_lying_back.keys,
        "times": put_hands_to_body_in_lying_back.times
    }, 200)
    
