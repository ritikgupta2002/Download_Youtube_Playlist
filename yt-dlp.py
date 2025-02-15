import os
import shutil
import yt_dlp
import subprocess

# Define the playlist URL and download directory
playlist_url = '' # ex = https://www.youtube.com/playlist?list=PL9ok7C7Yn9A-JaUtcMwevO_FfbFNRYLfU
download_dir = r''  # Correct path ex - D:\automation_videos\api testing

# Path to ffmpeg executable
ffmpeg_path = r'D:\ffmpeg\ffmpeg.exe'  # Ensure this is the correct path

# Create the directory if it doesn't exist
os.makedirs(download_dir, exist_ok=True)

# Download the playlist using yt-dlp
ydl_opts = {
    'format': 'bestvideo[height<=720]+bestaudio/best',  # Ensure 720p quality video and best audio
    'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # Output template
    'noplaylist': False,  # Handle playlists correctly
    'keepvideo': True,  # Do not delete original files after merging
    'ffmpeg_location': ffmpeg_path,  # Ensure yt-dlp uses the correct ffmpeg
}

# Download and process the playlist
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        ydl.download([playlist_url])  # Start the download
    except Exception as e:
        print(f"Error during download: {e}")
        exit(1)

# Check if files were downloaded
print(f"Files downloaded to: {download_dir}")

# Merge video and audio streams using FFmpeg
def merge_audio_video(video_file, audio_file):
    output_file = os.path.splitext(video_file)[0] + '_final.mp4'
    ffmpeg_command = [
        ffmpeg_path, '-i', video_file, '-i', audio_file, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_file
    ]
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Successfully merged {video_file} and {audio_file} into {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during merging: {e}")
        return None
    return output_file

# Process downloaded files to check for video and audio files
def process_downloaded_files():
    for root, dirs, files in os.walk(download_dir):
        for file in files:
            file_path = os.path.join(root, file)

            if file.endswith(('.mp4', '.webm')):  # Check if video file exists
                video_file = file_path
                audio_file = os.path.splitext(video_file)[0] + '.m4a'  # Assuming audio file has a similar name
                if os.path.exists(audio_file):
                    # If audio file exists, merge them
                    merged_file = merge_audio_video(video_file, audio_file)
                    if merged_file:
                        # Delete original MP4 and WebM files after successful merge
                        try:
                            os.remove(video_file)
                            os.remove(audio_file)
                            print(f"Deleted original files: {video_file}, {audio_file}")
                        except Exception as e:
                            print(f"Error deleting files: {e}")
                else:
                    print(f"Audio file not found for {video_file}, skipping merging.")
            else:
                print(f"Skipping unsupported file: {file_path}")

# Run the processing function
process_downloaded_files()

# Zip the directory containing the downloaded and merged videos
try:
    shutil.make_archive(download_dir, 'zip', download_dir)
    print(f'Playlist downloaded, audio and video merged, and zipped successfully. Find the zip file: {download_dir}.zip')
except Exception as e:
    print(f"Error while creating archive: {e}")
