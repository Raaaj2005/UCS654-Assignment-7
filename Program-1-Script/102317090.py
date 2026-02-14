import sys
import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment

def create_mashup():
    if len(sys.argv) != 5:
        print("Error: Wrong number of parameters.")
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        return

    singer_name = sys.argv[1]

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
        output_file = sys.argv[4]
    except ValueError:
        print("Error: Number of videos and duration must be integers.")
        return

    if num_videos <= 10:
        print("Error: Number of videos must be greater than 10.")
        return
    if duration <= 20:
        print("Error: Duration must be greater than 20.")
        return

    if not output_file.endswith(".mp3"):
        output_file += ".mp3"

    search_query = f"ytsearch{num_videos}:{singer_name}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'temp_audio_%(id)s.%(ext)s',
        'quiet': True,
    }

    temp_files = []

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)
            for entry in info['entries']:
                temp_files.append(f"temp_audio_{entry['id']}.mp3")

        combined = AudioSegment.empty()

        for file in temp_files:
            if os.path.exists(file):
                audio = AudioSegment.from_file(file)
                cut_audio = audio[:duration * 1000]
                combined += cut_audio

        combined.export(output_file, format="mp3")
        print(f"Success: Mashup saved as {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        for file in temp_files:
            if os.path.exists(file):
                os.remove(file)

if __name__ == "__main__":
    create_mashup()
