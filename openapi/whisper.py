from openai import OpenAI

from config.app_config import Config


def transcribe_audio(file_path, output_file, config:Config):
    """Transcribes an audio file using OpenAI Whisper API and writes output to a file."""

    client = OpenAI(api_key=config.openai.api_key)
    print(">>>>>>>>> Calling openai whisper api")

    with open(file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format= "verbose_json",
            language="en",
            timestamp_granularities=["word"]
        )

    # Write response to a file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(response.to_json())

    print(f"Transcription saved to {output_file}")
