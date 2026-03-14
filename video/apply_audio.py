import subprocess

def apply_audio(video_file, audio_file, duration, output_file):
    command = [
        'ffmpeg', '-i', video_file, '-i', audio_file, '-c:v', 'copy', '-c:a', 'aac',
        '-map', '0:v:0', '-map', '1:a:0', '-t', str(duration), output_file
    ]

    subprocess.run(command)
