# Automated AI Video Generator

Automated AI Video Generator is a Python-based tool for generating long-form videos from text stories. It automates the process of converting written narratives into engaging videos with narration, subtitles, background footage, and thumbnails. Perfect for creating content like Kids story videos or similar narrative formats.

## Features

- **Text-to-Speech**: Uses OpenAI's TTS API to generate high-quality narration from text stories
- **Automatic Subtitles**: Transcribes audio using OpenAI Whisper and creates ASS subtitle files with precise timing
- **Video Generation**: Combines narration, subtitles, and background video clips using MoviePy
- **Background Audio**: Supports background music mixing with adjustable volume
- **Thumbnail Creation**: Generates custom thumbnails for videos
- **Multiple Themes**: Supports different video themes (Minecraft, Subway)
- **Configurable**: Highly customizable through YAML configuration

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```

3. Set up OpenAI API key:
   - Create a `.env` file in the root directory
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

## Usage

### Basic Usage

Run the main script with a text file containing your story:

```bash
python long_form.py path/to/your/story.txt --type minecraft
```

### Command Line Options

- `file`: Path to the input text file (required)
- `--type`: Video theme type (`minecraft` or `subway`, default: `minecraft`)
- `--subtitle`: Path to custom subtitle file (optional)
- `--audio`: Path to custom audio file (optional)

### Input File Format

The input text file should follow this format:

```
Story Title Here
$$$
Story content here. This is the full narrative text that will be converted to speech and video.
```

### Output

The tool creates a working directory with intermediate files and outputs the final video file.

## Configuration

Edit `application.yml` to customize:

- **Working Directory**: Default location for processing files
- **Video Settings**: Resolution, FPS, output directory
- **Audio Settings**: Voice type, volume levels for main and background audio
- **Subtitle Settings**: Font, size, colors, positioning
- **Thumbnail Settings**: Template image and output directory

## Dependencies

- Python 3.x
- OpenAI API account and API key
- FFmpeg (for video processing)

## Project Structure

```
automated-ai-video-generator/
├── application.yml          # Configuration file
├── long_form.py             # Main entry point
├── requirement.txt          # Python dependencies
├── audio/                   # Audio processing modules
├── config/                  # Configuration handling
├── db/                      # Database operations
├── image/                   # Image/thumbnail processing
├── openapi/                 # OpenAI API integrations
├── process/                 # Main video creation logic
├── scripts/                 # Utility scripts
├── subtitle/                # Subtitle generation
├── video/                   # Video processing
├── zaudios/                 # Background audio files
├── zdownloads/              # Download directory
├── zfiles/                  # Input story files
├── zimages/                 # Image assets
└── zvideos/                 # Background video clips
    ├── minecraft/
    └── subway/
```

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

[Add your license here]</content>