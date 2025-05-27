import cv2
import matplotlib.pyplot as plt
import time

myCameras = [2, 4, 6, 8, 10, 12]
caps = [cv2.VideoCapture(i) for i in myCameras]

plt.ion()
fig, axs = plt.subplots(2, 3)
ims = [ax.imshow([[0]], vmin=0, vmax=255) for ax in axs.flat]

while True:
    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        if ret:
            ims[i].set_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            axs.flat[i].set_title(f"Camera {myCameras[i]}")
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.05)
