#!/usr/bin/env python3
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
from datetime import datetime
import os
import time

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

encoder = H264Encoder(bitrate=10000000)
output = "test.h264"


def manage_storage():
    dir_path = 'videos'
    files = sorted([os.path.join(dir_path, f) for f in os.listdir(dir_path)], key=os.path.getctime)
    total_size = sum(os.path.getsize(f) for f in files) / (1024 * 1024)  # Size in MB
    max_size = 20000  # Max storage size in MB
    while total_size > max_size and files:
        os.remove(files.pop(0))
        total_size = sum(os.path.getsize(f) for f in files) / (1024 * 1024)

while True:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = f'videos/video_{timestamp}.h264'
    print(f"Start Recording to {output}...")
    picam2.start_recording(encoder, output)

    time.sleep(600)
    picam2.stop_recording()
    manage_storage()

