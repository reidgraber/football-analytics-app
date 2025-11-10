import streamlit as st
from compressor import compress_video
from converter import convert_video_format, video_to_csv

st.title("🎞️ Football Video Tools: Compressor & Converter")

uploaded_file = st.file_uploader("Upload your video", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file:
    input_path = uploaded_file.name
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    action = st.selectbox("Choose an action:", ["Compress to 200MB", "Convert Format", "Convert to CSV (frame data)"])

    if st.button("Run"):
        if action == "Compress to 200MB":
            output = "compressed.mp4"
            compress_video(input_path, output)
            st.success("✅ Compression complete!")
            st.video(output)
            st.download_button("Download Compressed Video", open(output, "rb"), file_name=output)

        elif action == "Convert Format":
            format_choice = st.selectbox("Choose output format", ["mp4", "mov", "avi", "mkv"])
            output = f"converted.{format_choice}"
            convert_video_format(input_path, output, target_format=format_choice)
            st.success("✅ Conversion complete!")
            st.video(output)
            st.download_button("Download Converted Video", open(output, "rb"), file_name=output)

        elif action == "Convert to CSV (frame timestamps)":
            output = "video_data.csv"
            video_to_csv(input_path, output)
            st.success("✅ Video converted to CSV!")
            st.download_button("Download CSV", open(output, "rb"), file_name=output)

