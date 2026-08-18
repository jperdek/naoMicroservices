import os
from naoqi import ALProxy
import dotenv
import time

if os.environ.get("LOCAL", "True") == "True":
    dotenv.load_dotenv()

    
def set_voice_lines(voice_lines_config):
    if not g.speech_proxy:
        NAO_IP = os.environ.get("NAO_IP", "127.0.0.1")
        NAO_PORT = int(os.environ.get("NAO_PORT", 9559))
        g.speechProxy = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
    if "speed" in voice_lines_config:
        g.speechProxy.setParameter("speed", voice_lines_config["speed"])
    elif "lang" not in voice_lines_config or voice_lines_config["lang"] == "en":
            g.speechProxy.setParameter("speed", 80)
        elif voice_lines_config["lang"] == "sk":
            g.speechProxy.setParameter("speed", 100)

    for voice_line_config in voice_lines_config["voice_lines_configs"]:
        if "wait" in voice_line_config and voice_line_config["wait"]:
            time.sleep(voice_line_config["wait"])
        g.speechProxy.say(voice_line_config["voice_line"])
 