
import os
import re

from moviepy import AudioFileClip, concatenate_audioclips
from config.app_config import Config
from openapi.tts import text_to_audio


def file_text_to_audio(text, output_file, config: Config):
    working_dir = config.working_dir

    # Split text into sentence-based chunks
    text_chunks = split_text_into_sentences(text, max_length=3900)
    audio_files = []

    # Convert each chunk into speech
    for i, chunk in enumerate(text_chunks):
        temp_audio_path = os.path.join(working_dir, f'chunk-{i}_{config.timestamp}.mp3')
        text_to_audio(chunk, temp_audio_path, config)
        audio_files.append(temp_audio_path)

    # Concatenate audio files into final output
    audio_clips = [AudioFileClip(audio) for audio in audio_files]
    final_audio = concatenate_audioclips(audio_clips)

    final_audio.write_audiofile(output_file, codec="mp3")

    print(f"Speech saved to {output_file}")


def split_text_into_sentences(text, max_length=3900):
    # text = text.replace("\n", "    ")  # Replace newlines with 4 spaces
    sentences = re.split(r'(?<=[.!?])\s+', text)  # Split on sentence-ending punctuation
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            chunks.append(current_chunk)
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

