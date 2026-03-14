import random
import datetime
import json
from turtledemo.penrose import start

from config.app_config import Config


# Function to convert seconds to ASS time format
def convert_seconds_to_ass_time(seconds):
    time_delta = datetime.timedelta(seconds=seconds)
    hours, remainder = divmod(time_delta.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{seconds:04.2f}"


def group_words_into_sentences(words):
    final = []
    temp = []
    for word in words:
        if len(temp) == 0:
            temp.append(word)
        elif (word['start'] - temp[-1]['end']) > 0.1:
            start = temp[0]['start']
            end = word['start']
            final.append({'start':start, 'end': end, 'words': temp})
            temp = [word]
        else:
            temp.append(word)

    if len(temp) > 0:
        start = temp[0]['start']
        end = temp[-1]['end']
        final.append({'start': start, 'end': end, 'words': temp})
    return final

def highlight_word(word):
    return f"{{\\c&H00de00&}}{word}{{\\r}}"


def get_segments(words,sentence_end, max_words_per_line=10, max_chars_per_line=20, max_duration_per_subtitle=5):
    split_segments = []
    current_chunk = []
    current_start_time = words[0]["start"]
    current_char_count = 0

    for i, word in enumerate(words):
        current_chunk.append(word)
        current_char_count += len(word["word"])
        next_start_time = words[i + 1]["start"] if i + 1 < len(words) else word["end"]
        chunk_duration = next_start_time - current_start_time

        # Check if the current chunk exceeds word, character, or time constraints
        if (
                len(current_chunk) >= max_words_per_line
                or current_char_count > max_chars_per_line
                or chunk_duration >= max_duration_per_subtitle
        ):
            split_segments.append((current_chunk, current_start_time, next_start_time))
            current_chunk = []
            current_start_time = next_start_time
            current_char_count = 0

    # Add the remaining chunk
    if current_chunk:
        split_segments.append((current_chunk, current_start_time, words[-1]["end"]))

    last_end = split_segments[-1][2]
    last_end = sentence_end - 0.25 if (sentence_end - 0.25) > last_end else last_end;

    split_segments[-1] = (split_segments[-1][0], split_segments[-1][1], last_end)

    return split_segments


def generate_ass_subtitles(response, config:Config):
    alignment = 2
    if config.subtitle.position == "center":
        alignment = 5




    subtitles = []

    # ASS header
    subtitles.append("[Script Info]")
    subtitles.append("Title: Dynamic Highlight Duration Subtitles (Hindi)")
    subtitles.append("ScriptType: v4.00+")
    subtitles.append("")
    subtitles.append("[V4+ Styles]")
    subtitles.append(
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding")
    subtitles.append(
        f"Style: Default,Concert One,33,&HFFFFFF,&HFFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,4,4,{alignment},10,10,40,1")
    subtitles.append(
        "Style: Highlight,Concert One,28,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64FF00FF,0,0,0,0,100,100,0,0,1,1,2,2,10,10,40,1")
    subtitles.append("")
    subtitles.append("[Events]")
    subtitles.append("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")

    # first align subtitle time with audio:
    words = response["words"]

    sentences = group_words_into_sentences(words)

    # create ass format
    for sentence in sentences:
        # Split the segment into smaller chunks based on constraints
        split_segments = get_segments(sentence['words'], sentence['end'])
        full_sentence = ""
        for chunk, start_time, end_time in split_segments:
            for hid, hword in enumerate(chunk):
                for id, word in enumerate(chunk):
                    w = word['word']
                    if hid == id:
                        w = highlight_word(w)
                    full_sentence = full_sentence + " " + w
                start = convert_seconds_to_ass_time(hword['start'])
                end = end_time if (len(chunk) - 1) == hid else hword['end']
                end = convert_seconds_to_ass_time(end)
                subtitles.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{full_sentence}")
                full_sentence = ""

            # Add the ASS dialogue entry
    return "\n".join(subtitles)


# Main script to read Whisper JSON file and generate ASS file
def process_whisper_to_ass(input_file, output_file,  config:Config):
    # Read Whisper JSON data from file
    with open(input_file, "r", encoding="utf-8") as file:
        response = json.load(file)

    # Generate ASS subtitle content
    ass_content = generate_ass_subtitles(response, config)

    # Write to an .ass file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(ass_content)

    print(f"ASS subtitle file created successfully: {output_file}")
