import cv2
import numpy as np
import matplotlib.pyplot as plt

cam_ids = (2, 4, 6, 8, 10, 12) #range(1, 9)
rows, cols = 2, 3                  # 2×3 grid (6 slots)
w, h = 640, 480                    # capture size

plt.ion()
fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 3))
ims = [ax.imshow(np.zeros((h, w, 3), dtype=np.uint8)) for ax in axes.flat]
for ax in axes.flat:
    ax.axis("off")

def grab_once(cid):
    cap = cv2.VideoCapture(f"/dev/video{cid}")
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    ok, frame = cap.read()
    cap.release()
    if ok and frame is not None:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return None

for idx in range(0, len(cam_ids), 2):          # two cams at a time
    pair = cam_ids[idx : idx + 2]
    for j, cid in enumerate(pair):
        frame = grab_once(cid)
        slot = idx + j
        if slot >= len(ims):                   # ignore >6 cams
            continue
        if frame is not None:
            ims[slot].set_data(frame)
            axes.flat[slot].set_title(f"cam {cid}")
        else:
            axes.flat[slot].set_title(f"cam {cid} ERR")
    fig.canvas.draw_idle()
    plt.pause(0.001)

plt.ioff()
plt.show()
