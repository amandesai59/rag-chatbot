import os
import sys
import subprocess
import webvtt

def download_subtitles(video_url, video_id):
    print("⏬ Downloading subtitles...")
    command = [
        "yt-dlp",
        "-o", f"{video_id}.%(ext)s",
        "--write-auto-sub",
        "--skip-download",
        "--sub-lang", "en",
        video_url
    ]
    subprocess.run(command, check=True)

def convert_vtt_to_txt(video_id):
    vtt_file = f"{video_id}.en.vtt"
    output_dir = "docs"
    os.makedirs(output_dir, exist_ok=True)
    txt_file = os.path.join(output_dir, f"{video_id}.txt")

    if not os.path.exists(vtt_file):
        raise FileNotFoundError(f"{vtt_file} not found.")

    print("🧹 Cleaning and converting to .txt...")

    seen = set()
    with open(txt_file, "w", encoding="utf-8") as out:
        for caption in webvtt.read(vtt_file):
            lines = caption.text.strip().splitlines()
            for line in lines:
                line = line.strip()
                if line and line not in seen:
                    out.write(line + "\n")
                    seen.add(line)

    # ✅ Delete the original .vtt file
    os.remove(vtt_file)
    print(f"🗑️ Deleted: {vtt_file}")
    print(f"✅ Transcript saved as: {txt_file}")


def extract_video_id(url_or_id):
    if "watch?v=" in url_or_id:
        return url_or_id.split("watch?v=")[-1].split("&")[0]
    elif "youtu.be/" in url_or_id:
        return url_or_id.split("youtu.be/")[-1].split("?")[0]
    else:
        return url_or_id  # assume it's already a video ID

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_transcript.py <YouTube video URL or ID>")
        sys.exit(1)

    input_arg = sys.argv[1]
    video_id = extract_video_id(input_arg)

    try:
        download_subtitles(input_arg, video_id)
        convert_vtt_to_txt(video_id)
    except Exception as e:
        print(f"❌ Error: {e}")
