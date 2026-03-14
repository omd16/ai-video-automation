from moviepy.audio import fx as afx
from moviepy import AudioFileClip, CompositeAudioClip, VideoFileClip, AudioArrayClip, AudioClip

from config.app_config import Config


def create_audio(main_audio, back_audio, output_file, config:Config, composite_audio=None):
    main_audio_clip = AudioFileClip(main_audio)
    back_audio_clip = AudioFileClip(back_audio)
    length = main_audio_clip.duration

    # repeat
    back_audio_clip = back_audio_clip.with_effects([afx.AudioLoop(duration=length)])
    # volume
    main_audio_clip = main_audio_clip.with_volume_scaled(config.audio.main.volume)
    back_audio_clip = back_audio_clip.with_volume_scaled(config.audio.back.volume)

    composite_audio = CompositeAudioClip([main_audio_clip, back_audio_clip])

    composite_audio.write_audiofile(output_file)

    print(f"Main Combined audio written to {output_file}")
    return output_file