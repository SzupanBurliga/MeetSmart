import cv2
import numpy as np
import os

def get_frames(input_video_path, output_folder):
    """
    Extract unique frames from a video as separate images and save them with timestamps in the filenames.

    Args:
        input_video_path (str): The path to the input video file.
        output_folder (str): The folder where unique frames will be saved.
    """

    # Clear existing files in the output folder
    for filename in os.listdir(output_folder):
        file_path = os.path.join(output_folder, filename)
        if os.path.isfile(file_path):  # Ensure it's a file and not a subdirectory
            os.remove(file_path)

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
    last_saved_timestamp = -2  # Ensure the first frame is not restricted

    # Get the frame rate of the video to calculate timestamps
    fps = cap.get(cv2.CAP_PROP_FPS)

    while True:
        # Read a new frame from the video
        ret, frame = cap.read()
        
        if not ret:
            break  # End of video

        # Get the current timestamp in seconds from the original video
        current_timestamp_seconds = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # Convert milliseconds to seconds

        # Convert the frame to grayscale to compare easily
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # If it's not the first frame, compare it with the previous frame
        if prev_frame is not None:
            # Compute the correlation coefficient between the current and previous frame
            correlation = np.corrcoef(gray_frame.flatten(), prev_frame.flatten())[0, 1]

            # If the correlation is below a certain threshold and at least 2 seconds have passed, save the frame
            if correlation < 0.98 and (current_timestamp_seconds - last_saved_timestamp >= 2):
                # Save the frame as an image with the timestamp in the filename
                timestamp_str = f"{current_timestamp_seconds:.2f}"  # Format the timestamp to two decimal places
                output_image_path = os.path.join(output_folder, f"frame_{timestamp_str}s.png")
                cv2.imwrite(output_image_path, frame)
                saved_frame_count += 1
                last_saved_timestamp = current_timestamp_seconds  # Update last saved timestamp
                print(f"Saved: {output_image_path}")

        # Set the current frame as the previous frame for the next comparison
        prev_frame = gray_frame

    # Release the video capture object
    cap.release()

    print(f"Extraction completed. {saved_frame_count} unique frames saved.")


#get_frames("uploads/test.mkv", "outputs/unique_frames")  # Example usage
