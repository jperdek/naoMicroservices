#!/usr/bin/env python3
"""
nao_pose_service.py

Flask microservice that:
    - /arms/from_image: accept a single image, compute pose, send to NAO.
    - /arms/from_video: accept a video, split into frames via pose_from_video,
                        filter incomplete frames, send each valid pose to NAO,
                        save debug frame images.
"""
from flask import Flask
import flask_cors

from naoPoses.forearms_in_sitting.leg.forearm_leg_lifting_api import forearm_in_sitting_leg_api
from naoPoses.forearms_in_sitting.knee.forearm_knee_lifting_api import forearm_in_sitting_knee_api
from naoPoses.t_pose_knee_lifting.t_pose_knee_lifting_api import t_pose_knee_lifting_api
from naoPoses.lying.only_legs_up.only_legs_up_api import only_legs_up_api
from naoPoses.lying.cross_forefooting.cross_forefooting_api import cross_forefooting_api
from naoPoses.sitting.sitting_api import sitting_api
from naoPoses.arm_circling.arm_circling_in_standing_api import arm_circling_in_standing_api
from naoPoses.sitting.return_to_pose_in_sitting.return_to_pose_in_sitting_api import return_to_pose_in_sitting_api
from naoPoses.getting_up_from_chair.getting_up_from_chair_api import getting_up_from_chair_api


# =========================
# CONFIG
# =========================

SET_POSE_URL = "http://naorobotapi:5000/setting_pose/setCodedPose"

# Host directory mounted into pose container as /images
POSE_HOST_ROOT = "/home/ubuntu/Pictures"      # host/VM path
POSE_CONT_ROOT = "/images"                    # container path
IP_NAO = ""
PORT_NAO = "9449"

app = Flask(__name__)

flask_cors.CORS(app)
#

#standing
app.register_blueprint(t_pose_knee_lifting_api, url_prefix="/t_pose_knee_lifting_api/")

#sitting
app.register_blueprint(sitting_api, url_prefix="/sitting")
app.register_blueprint(return_to_pose_in_sitting_api, url_prefix="/return_to_pose_in_sitting")
app.register_blueprint(forearm_in_sitting_leg_api, url_prefix="/forearm_in_sitting_leg")
app.register_blueprint(getting_up_from_chair_api, url_prefix="/getting_up_from_chair")
#arm circling
app.register_blueprint(forearm_in_sitting_knee_api, url_prefix="/forearm_in_sitting_knee")
# arm circling in standing
app.register_blueprint(arm_circling_in_standing_api, url_prefix="/arm_circling_in_standing")

#lying
app.register_blueprint(cross_forefooting_api, url_prefix="/lying/cross_forefooting")
app.register_blueprint(only_legs_up_api, url_prefix="/lying/legs_up")


# =========================
# ROUTES
# =========================

@app.route("/test", methods=["GET"])
def test():
    return "NAO Coded Pose Operator Service is running."


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=False)
