import os.path

from config.app_config import Config
from openapi.whisper import transcribe_audio
from subtitle.whisper_to_ass import process_whisper_to_ass


def create_subtitle(audio_path, config:Config, given_subtitle=None):
    working_dir = config.working_dir
    subtitle_file = given_subtitle
    if not given_subtitle:
        subtitle_file = os.path.join(working_dir, f"subtitle_{config.timestamp}.json")
        transcribe_audio(audio_path, subtitle_file, config)

    ass_file = os.path.join(working_dir, f"subtitle_{config.timestamp}.ass")
    process_whisper_to_ass(subtitle_file, ass_file, config)

    return ass_file
