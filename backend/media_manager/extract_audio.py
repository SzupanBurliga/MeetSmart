import ffmpeg
import os
def get_audio(video_path, audio_output_path):

    """
    Extract audio from a video file and save it as a separate audio file.
    
    Args:
        video_path (str): The path to the input video file.
        audio_output_path (str): The path where the output audio file should be saved.
    """
    if os.path.exists(audio_output_path):
        os.remove(audio_output_path)
    try:
        # Use ffmpeg to extract the audio from the video
        ffmpeg.input(video_path).output(audio_output_path, acodec='mp3').run()
        print(f"Audio extracted successfully. Saved as {audio_output_path}")
    except ffmpeg.Error as e:
        print(f"An error occurred while extracting audio: {e}")
        return None

# Example usage:
video_file_path = './uploads/recording.webm'  # Replace with your video file path
audio_file_path = './outputs/output_audio.mp3'  # Replace with desired audio output file path



