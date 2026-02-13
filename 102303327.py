import sys
import os
import subprocess
import yt_dlp

# -------------------- INPUT VALIDATION --------------------
def validate_inputs():
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("NumberOfVideos and AudioDuration must be integers.")
        sys.exit(1)

    if num_videos <= 10:
        print("Number of videos must be greater than 10.")
        sys.exit(1)

    if duration <= 20:
        print("Audio duration must be greater than 20 seconds.")
        sys.exit(1)

    output_file = sys.argv[4]

    return singer, num_videos, duration, output_file


# -------------------- DOWNLOAD VIDEOS --------------------
def download_videos(singer, num_videos):
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    ydl_opts = {
        'format': 'worstaudio/worst',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'restrictfilenames': True,
        'windowsfilenames': True,
        'retries': 10,
        'fragment_retries': 10,
        'socket_timeout': 30
    }

    search_query = f"ytsearch{num_videos}:{singer}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])


# -------------------- CONVERT + TRIM USING FFMPEG --------------------
def convert_and_trim(duration):
    for file in os.listdir("downloads"):
        input_path = os.path.join("downloads", file)

        if not os.path.isfile(input_path):
            continue

        output_path = input_path.rsplit(".", 1)[0] + ".mp3"

        command = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-t", str(duration),
            "-q:a", "0",
            "-map", "a",
            output_path
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        os.remove(input_path)


# -------------------- MERGE FILES --------------------
def merge_audios(output_file):
    with open("filelist.txt", "w", encoding="utf-8") as f:
        for file in os.listdir("downloads"):
            if file.endswith(".mp3"):
                f.write(f"file 'downloads/{file}'\n")

    command = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "filelist.txt",
        "-c", "copy",
        output_file
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove("filelist.txt")


# -------------------- MAIN --------------------
def main():
    try:
        singer, num_videos, duration, output_file = validate_inputs()
        download_videos(singer, num_videos)
        convert_and_trim(duration)
        merge_audios(output_file)
        print("Mashup created successfully!")

    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
