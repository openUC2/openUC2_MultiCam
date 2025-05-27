import imageio as iio
import numpy as np

CAM_IDs = [2, 4, 6, 8, 10, 12]
ffmpeg_opts = [
    "-f", "v4l2",
    "-video_size", "640x480",
    "-pixel_format", "yuyv422",      # use a format your cam advertises
    "-framerate", "30",
    "-io_mode", "mmap",              # <-- crucial: avoid DMA-BUF
    "-thread_queue_size", "8"        # keep the driver buffer small
]

devices = [
    iio.get_reader(f"<video{cid}>",
                   format="ffmpeg",
                   ffmpeg_params=ffmpeg_opts)
    for cid in CAM_IDs
]

for cam in devices:
    frame = cam.get_next_data()      # first decoded frame
    print(frame.shape, frame.dtype)  # sanity check

for cam in devices:
    cam.close()
