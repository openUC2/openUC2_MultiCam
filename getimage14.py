import cv2
import time

cam_ids = [2, 4, 6, 8, 10, 12] #range(1, 9)
caps = {}

# open every /dev/videoX once, keep those that work
for cid in cam_ids:
    cap = cv2.VideoCapture(f"/dev/video{cid}")
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # light-weight
    if cap.isOpened():
        ok, frame = cap.read()
        if ok and frame is not None:
            caps[cid] = cap
            cv2.namedWindow(f"cam {cid}", cv2.WINDOW_NORMAL)
            cv2.imshow(f"cam {cid}", frame)
        else:
            print(f"cam {cid}: no image"); cap.release()
    else:
        print(f"cam {cid}: open failed")

if not caps:
    print("no cameras found")
    raise SystemExit

print("press Esc to quit")
while True:
    for cid, cap in list(caps.items()):
        ok, frame = cap.read()
        if not ok:
            print(f"cam {cid}: read failed")
            cap.release()
            del caps[cid]
            cv2.destroyWindow(f"cam {cid}")
            continue
        cv2.imshow(f"cam {cid}", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27 or not caps:   # Esc or all cams gone
        break

for cap in caps.values():
    cap.release()
cv2.destroyAllWindows()
