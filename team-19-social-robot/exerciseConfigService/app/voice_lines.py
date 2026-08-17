
import os
import json
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
                sound_in_base64: str, file_name: str) -> dict:
    """
    Inserts voice lines into specific frame config json
    Returns the updated config dict.
    """
    if not exercise_exists(exercise_id):
        raise FileNotFoundError(f"Exercise '{exercise_id}' not found")

    path = frame_path(exercise_id, frame_index)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Frame {frame_index} not found in exercise '{exercise_id}'")

    frame_assets_dir = frames_assets_dir(exercise_id, frame_index)
    sound_file_location = os.path.join(frame_assets_dir, file_name)
    if not os.path.exists(sound_file_location):
        os.makedirs(sound_file_location)
    audio = base64.b64decode(sound_in_base64)
    with open(sound_file_location, "wb") as file:
        file.write(audio)
    return frame_config


def get_voice_lines_sound(exercise_id: str, frame_index: int, file_name: str) -> Optional[str]:
    """
    Returns voice lines config from exercise config
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
        fileContent = file.read()
        audio_in_base64 = base64.b64encode(audio_in_base64)
    return audio_in_base64

