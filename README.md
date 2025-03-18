* Dashcam

Used for either my Car or Bike to loop record.

https://github.com/map7/dashcam

** Hardware

- Raspberry PI 4
- PI Camera V1
- Sdcard 64GB Sandisk Endurance
- [[https://shop.pimoroni.com/products/onoff-shim?variant=41102600138][OnOffshim]]
- 2 x Buttons & LED

*** Pin Connections
| Component | Pin |
|-----------|-----|
| Record Button | 33 |
| Shutdown Button | 29 |
| Status LED | 35 |

** Configuration Options

Configurable with command-line options:
#+begin_src
--max-storage 20GB      # Storage limit (20GB, 500MB, etc.)
--recording-duration 600      # Seconds per video segment
--bitrate 10000000      # Video bitrate
--width 1920      # Video width
--height 1080      # Video height
--framerate 30      # Frames per second
--output-dir videos      # Directory to store videos
--output-prefix video_      # Filename prefix for videos
#+end_src

** Usage

- Boot
- Hit the record button, LED should start
- Videos are kept in /home/pi/dashcam/videos
- System automatically manages storage, deleting oldest files first

See [[file:TODO.md][TODO.md]] for planned improvements.
