import json
from flask import Blueprint, request

from voice_lines import set_voice_lines


def application_json_response(payload, status):
    return json.dumps(payload), status, {"content-type": "application/json"}


def text_response(payload, status=200):
    return payload, status, {"content-type": "plain_text"}


voice_lines_api = Blueprint("voice_lines_api", __name__, template_folder="templates")


@voice_lines_api.route("/applyVoiceLine", methods=["POST"])
def set_pose():
    data = request.get_json(force=True)
    voice_lines_config = data["voice_lines"]
    set_voice_lines(voice_lines_config)
    return application_json_response({"success": True}, 200)

