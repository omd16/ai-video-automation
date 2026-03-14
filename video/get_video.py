import copy
import os
import random
import subprocess

from moviepy import VideoFileClip

from config.app_config import Config


def get_video(duration, v_type, config:Config):
    working_dir = config.working_dir
    video_dir = os.path.join(config.video.dir, v_type)
    files = [f for f in os.listdir(video_dir) if os.path.isfile(os.path.join(video_dir, f))]
    random.shuffle(files)
    files_store = copy.deepcopy(files)
    video_files = []
    if True:
        total_dur = 0
        while total_dur < duration:
            if len(files) == 0:
                files = copy.deepcopy(files_store)
            video_file = files.pop()
            video_path = os.path.join(video_dir, video_file)
            clip = VideoFileClip(video_path)
            video_duration = clip.duration
            clip.close()
            video_files.append(video_path)
            total_dur += video_duration
    output_dir = os.path.join(working_dir, f"video_{config.timestamp}.mp4")
    path = combine_video_files(video_files, output_dir, config.video.fps, working_dir)
    return path


def combine_video_files(video_files, output_file, fps, working_dir):

    input_txt_path = os.path.join(working_dir, "temp_video_list.txt")
    with open(input_txt_path, "w") as f:
        for file in video_files:
            f.write(f"file '{os.path.abspath(file)}'\n")

    command = [
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", input_txt_path,"-c", "copy", output_file
    ]
    subprocess.run(command, check=True)

    return output_file



