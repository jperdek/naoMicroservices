
import os
import json
import base64
from typing import Optional
from app.storage import (
    exercise_exists,
    frames_dir,
    frame_path
)

def _read_json(path: str):
    with open(path, "r") as f:
        return json.load(f)

def _write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
        
def frames_assets_dir(exercise_id: str, frame_index: str) -> str:
    return os.path.join(frames_dir(exercise_id), str(frame_index))


def insert_voice_lines_into_frame_config(exercise_id: str, frame_index: int,
                voice_lines_config: dict) -> dict:
    """
    Inserts voice lines into specific frame config json
    Returns the updated config dict.
    """
    if not exercise_exists(exercise_id):
        raise FileNotFoundError(f"Exercise '{exercise_id}' not found")

    path = frame_path(exercise_id, frame_index)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Frame {frame_index} not found in exercise '{exercise_id}'")

    frame_config = _read_json(path)
    frame_config["voice_lines"] = voice_lines_config
    _write_json(path, frame_config)
    return frame_config


def get_voice_lines_from_frame_config(exercise_id: str, frame_index: int) -> dict:
    """
    Returns voice lines config from exercise config
    """
    if not exercise_exists(exercise_id):
        raise FileNotFoundError(f"Exercise '{exercise_id}' not found")

    path = frame_path(exercise_id, frame_index)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Frame {frame_index} not found in exercise '{exercise_id}'")

    frame_config = _read_json(path)
    return frame_config.get("voice_lines", None)



def insert_voice_lines_sound(exercise_id: str, frame_index: int,
                sound_in_base64: str, file_name: str) -> None:
    """
    Saves webm sound into file and separate directory for particular frame
    Returns None
    """
    if not exercise_exists(exercise_id):
        raise FileNotFoundError(f"Exercise '{exercise_id}' not found")

    path = frame_path(exercise_id, frame_index)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Frame {frame_index} not found in exercise '{exercise_id}'")

    frame_assets_dir = frames_assets_dir(exercise_id, frame_index)
    sound_file_location = os.path.join(frame_assets_dir, file_name)
    if not os.path.exists(frame_assets_dir):
        os.makedirs(frame_assets_dir)
    if "base64," in sound_in_base64:
        sound_in_base64 = sound_in_base64.split("base64,")[1]
    audio = base64.b64decode(sound_in_base64)
   
    with open(sound_file_location, "wb") as file:
        file.write(audio)


def delete_voice_line_from_frame_config(exercise_id: str, frame_index: int, file_name: str) -> bool:
    """
    Deletes voice lines from specific frame config json
    Returns true if the record is successfully deleted otherwise false
    """
    if not exercise_exists(exercise_id):
        raise FileNotFoundError(f"Exercise '{exercise_id}' not found")

    path = frame_path(exercise_id, frame_index)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Frame {frame_index} not found in exercise '{exercise_id}'")

    frame_config = _read_json(path)
    frame_voice_lines = frame_config.get("voice_lines", {}).get("voice_lines_configs", {})
    found = False
    for key, values in frame_voice_lines.items():
        if "fileName" in values and values["fileName"] == fileName:
            del frame_voice_lines[key]
            found = True
            break
    if not found:
        return False
    _write_json(path, frame_config)
    return True


def get_voice_lines_sound(exercise_id: str, frame_index: int, file_name: str) -> Optional[str]:
    """
    Returns sound file encoded in base64
    """
    if not exercise_exists(exercise_id):
        raise FileNotFoundError(f"Exercise '{exercise_id}' not found")

    path = frame_path(exercise_id, frame_index)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Frame {frame_index} not found in exercise '{exercise_id}'")

    frame_assets_dir = frames_assets_dir(exercise_id, frame_index)
    sound_file_location = os.path.join(frame_assets_dir, file_name)
    if not os.path.exists(sound_file_location):
        return None
    with open(sound_file_location, "rb") as file:
        file_content = file.read()
        audio_in_base64 = base64.b64encode(file_content).decode("utf-8")
    return audio_in_base64


def delete_voice_lines_sound() -> bool:
    """
    Delete file with voice line and return true if so otherwise false
    """
    if not exercise_exists(exercise_id):
        raise FileNotFoundError(f"Exercise '{exercise_id}' not found")

    path = frame_path(exercise_id, frame_index)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Frame {frame_index} not found in exercise '{exercise_id}'")

    frame_assets_dir = frames_assets_dir(exercise_id, frame_index)
    sound_file_location = os.path.join(frame_assets_dir, file_name)
    if not os.path.exists(sound_file_location):
        return 
    os.remove(sound_file_location)
    return True
    