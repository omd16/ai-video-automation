import re


def combine_audio_files(output_file):
    audios = [
        r"C:\Users\Admin\prj\py\CapCut\temp_videos\working\test.mp4",
        r"C:\Users\Admin\prj\py\CapCut\temp_videos\working\test.mp4",
        r"C:\Users\Admin\prj\py\CapCut\temp_videos\working\test.mp4",
    ]

    # audio_clips = [VideoFileClip(audio) for audio in audios]
    # final_audio = concatenate_videoclips(audio_clips)
    #
    # final_audio.write_videofile(output_file, codec="libx264")
    # data = parse_file("test.txt")
    parts = None
    with open("test.txt", "r", encoding="utf-8") as file:
        parts = file.read().strip().split("$$$")
    data = split_text_into_sentences(parts[2])

    for i in data:
        print(i)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(f"Combined audio saved to: {output_file}")


# Call function
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

combine_audio_files("tests.mp4")
