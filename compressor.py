import ffmpeg
import os

def compress_video(input_path, output_path, target_size_mb=200):
    original_size = os.path.getsize(input_path) / (1024 * 1024)
    ratio = min(1, target_size_mb / original_size)
    bitrate = max(500, int(5000 * ratio))
    stream = ffmpeg.input(input_path)
    stream = ffmpeg.output(stream, output_path, **{
        'b:v': f'{bitrate}k',
        'preset': 'fast',
        'movflags': '+faststart'
    })
    ffmpeg.run(stream, overwrite_output=True)
    return output_path
