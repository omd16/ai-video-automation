import os
from datetime import datetime

import yaml
from pydantic import BaseModel
from typing import Optional


# Define Data Models
class OpenAIConfig(BaseModel):
    api_key: str

class VideoConfig(BaseModel):
    dir: str
    fps: int
    size: str

class AudioTrackConfig(BaseModel):
    dir: Optional[str] = None
    volume: float
    voice: Optional[str] = 'echo'

class AudioConfig(BaseModel):
    back: AudioTrackConfig
    main: AudioTrackConfig

class SubtitleConfig(BaseModel):
    font: str
    font_size: int
    color: str
    highlight_color: str
    preset: str
    position: str

class ThumbConfig(BaseModel):
    dir: str
    name: str

class Config(BaseModel):
    working_dir: str
    timestamp : Optional[str] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    openai: OpenAIConfig
    video: VideoConfig
    audio: AudioConfig
    subtitle: SubtitleConfig
    thumb: ThumbConfig


# Load YAML config
def load_config(file_path: str) -> Config:
    with open(file_path, "r") as file:
        raw_config = yaml.safe_load(file)

    # Replace environment variables
    for key, value in raw_config.get("openai", {}).items():
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value.strip("${}")
            raw_config["openai"][key] = os.getenv(env_var, f"Missing {env_var}")

    # Map to Pydantic model
    return Config(**raw_config)
