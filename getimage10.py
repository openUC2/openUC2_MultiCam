import imageio as iio
import matplotlib.pyplot as plt
import time

myCameras = [2, 4, 6, 8, 10, 12]

plt.ion()
fig, axs = plt.subplots(2, 3)
ims = []
for ax in axs.flat:
    im = ax.imshow([[0]], vmin=0, vmax=255)
    ims.append(im)

while True:
    for i, cam_id in enumerate(myCameras):
        try:
            reader = iio.get_reader(f"<video{cam_id}>")
            frame = reader.get_data(0)
            ims[i].set_data(frame)
            axs.flat[i].set_title(f"Camera {cam_id}")
            reader.close()
        except Exception as e:
            print(f"Camera {cam_id} error: {e}")
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.1)
