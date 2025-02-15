import os

# Define the download directory where the files are located
download_dir = r''  # Correct path ex- D:\automation_videos\selenium framework

def delete_video_files():
    # Walk through the directory and remove mp4 and webm files
    for root, dirs, files in os.walk(download_dir):
        for file in files:
            file_path = os.path.join(root, file)

            # Check if the file is a video file (.mp4 or .webm)
            if file.endswith(('.mp4', '.webm')):
                try:
                    os.remove(file_path)  # Delete the file directly
                    print(f"Deleted file: {file_path}")
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")

# Run the function to delete the video files
delete_video_files()
