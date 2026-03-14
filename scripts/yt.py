import argparse
import yt_dlp


def download_video_only(url, output_path=".", quality="137"):
    ydl_opts = {
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        "format": quality,  # Only download 1080p video (137)
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download 1080p YouTube video without audio.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--output", default="./zdownloads", help="Output directory (default: current directory)")
    parser.add_argument("--quality", default="137", help="Video quality (default: 1080p without audio)")
    args = parser.parse_args()

    download_video_only(args.url, args.output, args.quality)
