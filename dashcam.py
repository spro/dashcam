#!/usr/bin/env python3
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
from datetime import datetime
import os
import time
import argparse
import re
import signal
import sys


def parse_size(size_str):
    """Parse a size string like '20GB' or '500MB' to bytes"""
    match = re.match(r"^(\d+)([kmg]?b)$", size_str.lower())
    if not match:
        raise argparse.ArgumentTypeError(
            f"Invalid size format: {size_str}. Use format like '20GB' or '500MB'"
        )

    value, unit = match.groups()
    value = int(value)

    if unit == "b":
        return value
    elif unit == "kb":
        return value * 1024
    elif unit == "mb":
        return value * 1024 * 1024
    elif unit == "gb":
        return value * 1024 * 1024 * 1024
    else:
        raise argparse.ArgumentTypeError(f"Unknown unit: {unit}")


# Parse command line arguments
parser = argparse.ArgumentParser(description="Raspberry Pi Dashcam")
parser.add_argument(
    "--max-storage",
    type=str,
    default="20GB",
    help="Maximum storage size (e.g., 20GB, 500MB)",
)
parser.add_argument(
    "--recording-duration",
    type=int,
    default=600,
    help="Duration of each video segment in seconds (default: 600)",
)
parser.add_argument(
    "--bitrate",
    type=int,
    default=10000000,
    help="Video bitrate in bits per second (default: 10000000)",
)
parser.add_argument(
    "--width", type=int, default=1920, help="Video width in pixels (default: 1920)"
)
parser.add_argument(
    "--height", type=int, default=1080, help="Video height in pixels (default: 1080)"
)
parser.add_argument(
    "--framerate", type=int, default=30, help="Video framerate (default: 30)"
)
parser.add_argument(
    "--output-dir",
    type=str,
    default="videos",
    help="Directory to store video files (default: videos)",
)
parser.add_argument(
    "--output-prefix",
    type=str,
    default="video_",
    help="Prefix for video filenames (default: video_)",
)
args = parser.parse_args()

# Convert storage string to MB for internal use
max_storage_bytes = parse_size(args.max_storage)
max_storage_mb = max_storage_bytes / (1024 * 1024)

# Global variable to track if recording is active
recording_active = False
picam2 = None


def setup_camera():
    try:
        global picam2
        picam2 = Picamera2()
        video_config = picam2.create_video_configuration(
            main={"size": (args.width, args.height), "format": "RGB888"},
            controls={"FrameRate": args.framerate},
        )
        picam2.configure(video_config)
        return H264Encoder(bitrate=args.bitrate)
    except Exception as e:
        print(f"Error setting up camera: {e}")
        sys.exit(1)


# Set up camera and encoder
encoder = setup_camera()
output = "test.h264"


# Handle graceful shutdown
def signal_handler(sig, frame):
    print("Shutting down...")
    if recording_active and picam2:
        try:
            picam2.stop_recording()
        except Exception as e:
            print(f"Error stopping recording: {e}")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def manage_storage():
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Created directory: {args.output_dir}")

    # Get all files in directory
    files = sorted(
        [os.path.join(args.output_dir, f) for f in os.listdir(args.output_dir)],
        key=os.path.getctime,
    )
    total_size = sum(os.path.getsize(f) for f in files) / (1024 * 1024)  # Size in MB

    # Remove oldest files if over size limit
    while total_size > max_storage_mb and files:
        oldest_file = files.pop(0)
        print(f"Removing oldest file: {oldest_file}")
        os.remove(oldest_file)
        total_size = sum(os.path.getsize(f) for f in files) / (1024 * 1024)


while True:
    try:
        # Make sure output directory exists
        manage_storage()

        # Generate output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create full path combining output directory, prefix and timestamp
        output_path = os.path.join(
            os.path.abspath(args.output_dir), f"{args.output_prefix}{timestamp}.h264"
        )

        print(f"Start Recording to {output_path}...")

        # Update recording status
        recording_active = True
        picam2.start_recording(encoder, output_path)

        # Record for specified duration
        time.sleep(args.recording_duration)

        # Stop recording
        picam2.stop_recording()
        recording_active = False

        # Manage storage space
        manage_storage()
    except Exception as e:
        print(f"Error during recording: {e}")
        recording_active = False
        # Wait a moment before retrying
        time.sleep(5)
