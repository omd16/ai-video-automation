from openai import OpenAI

from config.app_config import Config


def text_to_audio(input_text, output_file, config:Config):
    """Transcribes an audio file using OpenAI Whisper API and writes output to a file."""

    client = OpenAI(api_key=config.openai.api_key)
    print(">>>>>>>>> Calling openai tts api")

    response = client.audio.speech.create(
        input= input_text,
        model="tts-1",
        voice=config.audio.main.voice,
        response_format="mp3",
        timeout= 300,
    )

    # Write response to a file
    response.write_to_file(output_file)

    print(f"Speech saved to {output_file}")
