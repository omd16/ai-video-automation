import os
import subprocess
import time


def reprocess_video(input_video, output_video,fps=24, size=(1920,1080)):
    w,h = size
    command = [
        "ffmpeg",
        # "-stream_loop", "-1",  # Loop indefinitely
        "-i", input_video,  # Input file
        # "-ss", str(start_time),  # Start time
        #"-t", str(duration),  # Duration
        "-vf", f"scale={w}:{h},fps={str(fps)}",  # Resize & set FPS
        "-c:v", "libx264",  # Video codec
        "-preset", "veryfast",  # Encoding speed
        "-crf", "18",  # Quality setting (lower = better)
        output_video  # Output file
    ]

    subprocess.run(command, check=True)
    return output_video


input_vid = r"C:\Users\Admin\prj\py\Reddtale\zdownloads\subway_official_5min.mp4"
output= r"C:\Users\Admin\prj\py\Reddtale\zvideos\subway\subway_official_5min.mp4"

size = (2048, 1152)
reprocess_video(input_vid, output, size = size)