# Dashcam Improvements

- [x] Make maximum storage size configurable with human-readable strings (like "20GB" or "500MB")
- [x] Create videos directory automatically if it doesn't exist
- [x] Make recording duration configurable
- [x] Make video settings (bitrate, resolution, framerate) configurable
- [x] Add error handling for file operations and camera failures
- [x] Implement graceful shutdown handling (catch SIGTERM)
- [x] Make output path configurable
- [ ] Replace print statements with proper logging
- [ ] Support MP4 format with container (currently raw H264)
- [ ] Add overlay with timestamp on video
- [ ] Implement button debouncing in monitor.py
- [ ] Add video retention options (keep files for X days vs size-based)