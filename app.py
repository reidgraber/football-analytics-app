import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import plotly.express as px

st.set_page_config(page_title="Football Film Analyzer", layout="wide")

st.title("🏈 Football Film Analyzer")
st.write("Upload your game film (.mp4) to analyze offensive and defensive intensity over time.")

uploaded_video = st.file_uploader("Upload Game Film", type=["mp4"])

if uploaded_video:
    # Save the uploaded file to a temporary location
    tfile = tempfile.NamedTemporaryFile(delete=False)
    with open(tfile.name, "wb") as f:
        f.write(uploaded_video.read())

    st.video(tfile.name)

    # OpenCV video capture
    cap = cv2.VideoCapture(tfile.name)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    duration = total_frames / fps if fps > 0 else 0

    st.write(f"🎥 **Duration:** {duration/60:.1f} minutes  |  **FPS:** {fps}  |  **Frames:** {total_frames}")

    progress_bar = st.progress(0)
    play_intensity = []
    prev_frame = None
    sample_rate = int(fps * 2)  # take 1 frame every ~2 seconds

    # Process in chunks
    for frame_num in range(0, total_frames, sample_rate):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if prev_frame is None:
            prev_frame = gray
            continue

        # Motion intensity between frames
        diff = cv2.absdiff(prev_frame, gray)
        score = np.sum(diff) / 1e6
        play_intensity.append(score)
        prev_frame = gray

        # Update progress
        progress_bar.progress(min(1.0, frame_num / total_frames))

    cap.release()
    progress_bar.empty()

    # Generate analytics chart
    frames = np.arange(len(play_intensity))
    data = {"Frame": frames, "Intensity": play_intensity}
    fig = px.line(data, x="Frame", y="Intensity",
                  title="Game Activity Intensity Over Time",
                  labels={"Frame": "Sample Frame", "Intensity": "Motion Intensity"})
    st.plotly_chart(fig, use_container_width=True)

    st.write("✅ **Analysis Complete!**")
    st.markdown("""
    ### 🧠 Quick Insights
    - **High spikes** → likely active plays (runs, passes, tackles)
    - **Flat lines** → time between plays or huddles
    - Works for long videos (even full games)
    """)

else:
    st.info("Upload an MP4 video to begin analysis.")
