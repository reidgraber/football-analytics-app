import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import plotly.express as px

st.set_page_config(page_title="Football Film Analyzer", layout="wide")

st.title("🏈 Football Film Analyzer")
st.write("Upload game film (.mp4) to analyze offensive and defensive performance.")

uploaded_video = st.file_uploader("Upload Game Film", type=["mp4"])

if uploaded_video:
    # Save video temporarily
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())
    
    # Display video preview
    st.video(tfile.name)
    
    # Video capture
    cap = cv2.VideoCapture(tfile.name)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    duration = frame_count / fps if fps > 0 else 0
    st.write(f"**Video length:** {duration:.2f} seconds | **FPS:** {fps}")

    st.write("🔍 Analyzing film... (this may take 1–2 minutes)")
    
    # Simple frame-by-frame motion detection
    play_intensity = []
    prev_frame = None

    frame_sample_rate = max(1, int(fps))  # sample 1 frame per second
    for i in range(0, frame_count, frame_sample_rate):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if prev_frame is None:
            prev_frame = gray
            continue
        frame_diff = cv2.absdiff(prev_frame, gray)
        motion_score = np.sum(frame_diff) / 1e6  # scaled motion
        play_intensity.append(motion_score)
        prev_frame = gray
    
    cap.release()
    
    st.success("✅ Film processed successfully!")

    # Convert to fake analytics
    frame_nums = list(range(len(play_intensity)))
    data = {"Frame": frame_nums, "Activity": play_intensity}
    
    fig = px.line(data, x="Frame", y="Activity",
                  title="Play Activity Intensity Over Time",
                  labels={"Frame": "Frame Sample", "Activity": "Motion Intensity"})
    st.plotly_chart(fig, use_container_width=True)

    st.write("""
    ### 🧠 Basic Interpretation:
    - **High spikes** in activity likely correspond to plays or tackles.  
    - **Low sections** often correspond to huddles or downtime.  
    - Future versions will automatically detect formation, run/pass type, and success rate.
    """)

else:
    st.info("Upload an MP4 video to begin analysis.")
