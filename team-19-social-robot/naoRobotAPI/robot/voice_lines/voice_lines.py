# -*- coding: utf-8 -*-
import os
from naoqi import ALProxy
import dotenv
import time
from flask import g
import string

if os.environ.get("LOCAL", "True") == "True":
    dotenv.load_dotenv()

    
def set_voice_lines(voice_lines_config):
    if "speech_proxy" not in g:
        NAO_IP = os.environ.get("NAO_IP", "127.0.0.1")
        NAO_PORT = int(os.environ.get("NAO_PORT", 9559))
        g.speech_proxy = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
    if "speed" in voice_lines_config:
        g.speech_proxy.setParameter("speed", voice_lines_config["speed"])
    elif "lang" not in voice_lines_config or voice_lines_config["lang"] == "en":
        g.speech_proxy.setParameter("speed", 80)
    elif voice_lines_config["lang"] == "sk":
        g.speech_proxy.setParameter("speed", 100)

    for _, voice_line_config in voice_lines_config["voice_lines_configs"].items():
        if "wait" in voice_line_config and voice_line_config["wait"]:
            time.sleep(voice_line_config["wait"])
        text = unicode(voice_line_config["translation"]).encode('utf8', 'replace')
        g.speech_proxy.say(text, "Czech")
 