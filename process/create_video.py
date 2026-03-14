import os.path
import random
import time

from moviepy import AudioFileClip

from audio.create_audio import create_audio
from audio.text_to_audio import file_text_to_audio
from config.app_config import Config
from image.thumb import create_thumb
from subtitle.create_subtitle import create_subtitle
from video.apply_audio import apply_audio
from video.apply_subtitle import add_subtitles_to_video
from video.get_video import get_video


def create_long_form_video(text_file, config: Config, v_type, subtitle=None, audio=None):
    pstart_time = time.time()  # Capture end time

    file_data = parse_file(text_file)

    main_aud, final_aud = __create_audio(file_data["STORY"], config, audio)
    print(f"<<<<<<<<<<< Audio created to:{final_aud}>>>>>>>>>>>")
    log_time(pstart_time)

    subtitle_file = __create_subtitle(main_aud, config, subtitle)
    print(f"<<<<<<<<<<< Subtitle file created:{subtitle_file}>>>>>>>>>>>")
    log_time(pstart_time)

    video_path = __create_video(final_aud, subtitle_file, config, v_type)
    print(f"<<<<<<<<<<< Video written to:{video_path}>>>>>>>>>>>")
    log_time(pstart_time)

    thumb_path = __create_thumb(file_data["TITLE"], config)
    print(f"<<<<<<<<<<< Video written to:{thumb_path}>>>>>>>>>>>")
    log_time(pstart_time)

    return video_path


def log_time(start):
    print(f"Time taken: {time.time() - start} seconds")


def __create_audio(text, config: Config, given_audio=None):
    working_dir = config.working_dir
    main_output_file = given_audio
    if not given_audio:
        main_output_file = os.path.join(working_dir, f"main_aud_{config.timestamp}.mp3")
        file_text_to_audio(text, main_output_file, config)
    back_music = get_random_file(config.audio.back.dir)
    final_output_file = os.path.join(working_dir, f"final_aud_{config.timestamp}.mp3")
    create_audio(main_output_file, back_music, final_output_file, config)

    return main_output_file, final_output_file


def __create_subtitle(input_aud_file, config: Config, subtitle=None):
    main_output_file = create_subtitle(input_aud_file, config, subtitle)
    return main_output_file


def __create_video(final_aud, subtitle_file, config: Config, v_type):
    clip = AudioFileClip(final_aud)
    duration = clip.duration
    clip.close()
    working_dir = config.working_dir

    video_path = get_video(duration, v_type, config)

    aud_output_dir = os.path.join(working_dir, f"video_{config.timestamp}_aud.mp4")
    apply_audio(video_path, final_aud, duration, aud_output_dir)

    sub_output_dir = os.path.join(working_dir, f"video_{config.timestamp}_aud_sub.mp4")
    add_subtitles_to_video(aud_output_dir, subtitle_file, sub_output_dir)
    return sub_output_dir


def __create_thumb(text, config: Config):
    working_dir = config.working_dir
    path = os.path.join(working_dir, f"thumbnail_{config.timestamp}.jpg")
    create_thumb(text, path, config)
    return path


def parse_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        parts = file.read().strip().split("$$$")

    if len(parts) < 3:
        raise ValueError("Invalid file format! Expected three sections separated by $$$")

    return {
        "TITLE": parts[0].strip(),
        "DESC": parts[1].strip(),
        "STORY": parts[2].strip()
    }


def get_random_file(directory):
    """Returns a random file from the given directory."""
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            raise FileNotFoundError("No files found in the directory.")
        return os.path.join(directory, random.choice(files))
    except Exception as e:
        print(f"Error: {e}")
        return None
