* Dashcam

Use a Raspberry Pi camera to do loop recording, for a dashcam or security.

Based on https://github.com/map7/dashcam

** Hardware

- Raspberry PI 4
- PI Camera V1
- 2 x Buttons & LED

*** Pin Connections

| Component | Pin |
|-----------|-----|
| Record Button | 33 |
| Shutdown Button | 29 |
| Status LED | 35 |

** Options

```
--max-storage 20GB        # Storage limit (20GB, 500MB, etc.)
--recording-duration 600  # Seconds per video segment
--bitrate 10000000        # Video bitrate
--width 1920              # Video width
--height 1080             # Video height
--framerate 30            # Frames per second
--output-dir videos       # Directory to store videos
--output-prefix video_    # Filename prefix for videos
```
