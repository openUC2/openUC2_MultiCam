import imageio as iio
import matplotlib.pyplot as plt
import time
import signal                             # so you can quit cleanly with Ctrl-C

myCameras = [2, 4, 6, 8, 10, 12]

# --- open the devices once ---------------------------------------------------
readers = []
for cam_id in myCameras:
    try:
        r = iio.get_reader(f"<video{cam_id}>")   # keep the handle
        readers.append(r)
    except Exception as e:                       # camera missing / busy
        print(f"Camera {cam_id} error on open: {e}")
        readers.append(None)

# --- draw setup --------------------------------------------------------------
plt.ion()
fig, axs = plt.subplots(2, 3)
ims = []
for ax in axs.flat:
    im = ax.imshow([[0]], vmin=0, vmax=255)
    ims.append(im)
    ax.set_xticks([]); ax.set_yticks([])

# --- graceful shutdown -------------------------------------------------------
running = True
def _stop(sig, frame):
    global running
    running = False
signal.signal(signal.SIGINT, _stop)

# --- main loop ---------------------------------------------------------------
while running:
    for i, r in enumerate(readers):
        if r is None:                # camera failed during open
            continue
        try:
            frame = r.get_next_data()  # grab latest frame without reopening
            ims[i].set_data(frame)
            axs.flat[i].set_title(f"Camera {myCameras[i]}")
        except Exception as e:         # camera unplugged while running, etc.
            print(f"Camera {myCameras[i]} error: {e}")
            r.close()
            readers[i] = None
    fig.canvas.draw_idle()
    plt.pause(0.001)                  # lets Matplotlib refresh without blocking
    time.sleep(0.05)

# --- cleanup -----------------------------------------------------------------
for r in readers:
    if r is not None:
        r.close()
plt.close(fig)
