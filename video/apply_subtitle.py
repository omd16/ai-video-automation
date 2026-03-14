import subprocess


def add_subtitles_to_video(input_video, subtitle_file, output_video):
    subtitle_file =  subtitle_file.replace("\\", "/")
    # ffmpeg command to add subtitles
    command = [
        'ffmpeg',
        '-i', input_video,  # Input video
        '-vf', f"ass={subtitle_file}",
        '-c:v', 'libx264',  # Use libx264 codec for video
        '-preset', 'ultrafast',  # Medium encoding preset
        # '-crf', '18',  # Set CRF value (quality)
        '-c:a', 'copy',  # Copy the audio stream without re-encoding
        output_video  # Output video file
    ]

    # Execute the ffmpeg command
    subprocess.run(command, check=True)
    print(f"Video with subtitles saved as: {output_video}")

    return output_video