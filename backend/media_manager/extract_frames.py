import ffmpeg
import cv2
import numpy as np
import os
import ffmpeg

def capture_slides(input_video_path, output_video_path):
    """
    Capture each slide from a presentation video and create a new video from these frames,
    where each frame lasts for 1 second and there is no audio.
    
    Args:
        input_video_path (str): The path to the input video file.
        output_video_path (str): The path where the new video should be saved.
    """
    try:
        # Capture frames with significant scene change and set output frame rate
        ffmpeg.input(input_video_path).output(
            output_video_path,
            vf='select=gt(scene\,0.05),setpts=N/TB,fps=1',  # Increased threshold for scene change
            r=1,  # Set output frame rate to 1 fps
        ).global_args('-an').run()  # Disable audio
        print(f"New video created successfully. Saved as {output_video_path}")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e}")
        return None


def extract_unique_frames(input_video_path, output_folder):
    """
    Extract unique frames from a video as separate images.
    
    Args:
        input_video_path (str): The path to the input video file.
        output_folder (str): The folder where unique frames will be saved.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    # Open the video using OpenCV
    cap = cv2.VideoCapture(input_video_path)
    
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    # Initialize variables
    prev_frame = None
    saved_frame_count = 0

    while True:
        # Read a new frame from the video
        ret, frame = cap.read()
        
        if not ret:
            break  # End of video
        
        # Convert the frame to grayscale to compare easily
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # If it's not the first frame, compare it with the previous frame
        if prev_frame is not None:
            # Compute the correlation coefficient between the current and previous frame
            correlation = np.corrcoef(gray_frame.flatten(), prev_frame.flatten())[0, 1]

            # If the correlation is below a certain threshold, save the frame
            if correlation < 0.98:  # Adjust this threshold as needed
                # Save the frame as an image
                output_image_path = os.path.join(output_folder, f"frame_{saved_frame_count}.png")
                cv2.imwrite(output_image_path, frame)
                saved_frame_count += 1
                print(f"Saved: {output_image_path}")
        
        # Set the current frame as the previous frame for the next comparison
        prev_frame = gray_frame

    # Release the video capture object
    cap.release()
    print(f"Extraction completed. {saved_frame_count} unique frames saved.")
# Example usage:
input_video_path = './uploads/recording.webm'  # Replace with your video file path
output_folder = './outputs/unique_frames'  # Folder where unique frames will be saved
cut_video_path = './outputs/cut_video.mp4'  # Path to save the cut


# Extract unique frames from the video
def get_frames():
    capture_slides(input_video_path, cut_video_path)
    extract_unique_frames(cut_video_path, output_folder)
