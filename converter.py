import ffmpeg
import os
import cv2
import csv

def convert_video_format(input_path, output_path, target_format="mp4"):
    if not output_path.endswith(f".{target_format}"):
        output_path += f".{target_format}"
    ffmpeg.input(input_path).output(output_path).run(overwrite_output=True)
    return output_path

def video_to_csv(input_path, output_csv="video_frames.csv", frame_skip=30):
    """Converts video into frame-level CSV data (timestamps, frame count, etc.)"""
    cap = cv2.VideoCapture(input_path)
    frame_data = []
    frame_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_id % frame_skip == 0:
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            frame_data.append([frame_id, timestamp])
        frame_id += 1

    cap.release()

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Frame_ID", "Timestamp_ms"])
        writer.writerows(frame_data)

    return output_csv
