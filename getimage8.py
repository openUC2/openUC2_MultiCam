import imageio as iio
import matplotlib.pyplot as plt
import time

myCameras = [2, 4, 6, 8, 10, 12]
camera_readers = []

# Open all cameras
for cam_id in myCameras:
    try:
        reader = iio.get_reader(f"<video{cam_id}>")
        camera_readers.append(reader)
    except Exception as e:
        print(f"Failed to open camera {cam_id}: {e}")
        camera_readers.append(None)

plt.ion()  # Interactive mode on
fig, axs = plt.subplots(2, 3)  # Adjust grid size depending on number of cameras

ims = []
for ax in axs.flat:
    im = ax.imshow([[0]], vmin=0, vmax=255)
    ims.append(im)

while True:
    for i, reader in enumerate(camera_readers):
        if reader is None:
            continue
        try:
            frame = reader.get_next_data()
            ims[i].set_data(frame)
            axs.flat[i].set_title(f"Camera {myCameras[i]}")
        except Exception as e:
            print(f"Error reading from camera {myCameras[i]}: {e}")
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.05)  # Adjust frame rate
