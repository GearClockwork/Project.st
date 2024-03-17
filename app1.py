import streamlit as st
import cv2
import tempfile
import os
from io import BytesIO
from PIL import Image

def extract_frames(video_path):
    """
    Extract frames from a video file.

    Args:
        video_path (str): Path to the video file.

    Returns:
        list: List of extracted frames in RGB format.
    """
    frames = []
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    success, image = vidcap.read()
    count = 0
    while success:
        if count % int(fps) == 0:
            frames.append(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB
        success, image = vidcap.read()
        count += 1

    vidcap.release()
    return frames

def main():
    """
    Main function for Streamlit application.
    """
    st.title("Video Frame Extractor")

    # Put file upload in the sidebar
    uploaded_video = st.sidebar.file_uploader("Upload Video", type=["mp4"])

    if uploaded_video is not None:
        # Display the uploaded video
        st.video(uploaded_video, format='video/mp4')

        # Extract frames from the uploaded video
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_video.read())
            temp_file_path = temp_file.name

        frames = extract_frames(temp_file_path)
        
        # Display frames in a grid layout
        st.subheader("Extracted Frames")

        num_frames = len(frames)
        num_columns = 4  # Adjust the number of columns as needed
        num_rows = (num_frames - 1) // num_columns + 1

        for i in range(num_rows):
            cols = st.columns(num_columns)
            for j in range(num_columns):
                idx = i * num_columns + j
                if idx < num_frames:
                    frame = frames[idx]
                    cols[j].image(frame, caption=f"Frame {idx + 1}", use_column_width=True)

        # Cleanup temporary file
        os.remove(temp_file_path)

if __name__ == "__main__":
    main()
