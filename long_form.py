import argparse
import os
import sys
from typing import List

from config.app_config import load_config
from process.create_video import create_long_form_video

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
    parser = argparse.ArgumentParser(description="Generate video with effects based on a CSV file.")
    parser.add_argument("file", help="Path to the file.")
    parser.add_argument("--type", default="minecraft", help="Parallel processing.")
    parser.add_argument("--subtitle", type=str, help="Directory to subtitle.")
    parser.add_argument("--audio", type=str, help="Directory to audio.")

    args = parser.parse_args()
    types = ["minecraft", "subway"]
    if args.type not in types:
        raise Exception("Please enter valid type")
    file = args.file
    config = load_config("application.yml")
    file_name = os.path.splitext(os.path.basename(file))[0]
    dir_path = os.path.join(config.working_dir, file_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        inp = input("Already processed, Do you want to reprocess? Type continue")
        if not inp == "continue":
            raise Exception("already processed!")
    config.working_dir = dir_path

    # Process the CSV and generate temporary video files
    video_path = create_long_form_video(
        file, config, args.type, args.subtitle, args.audio
    )

    print(f"Final video generated: {video_path}")


if __name__ == "__main__":
    main()
