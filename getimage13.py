import imageio as iio, matplotlib.pyplot as plt, os, time, signal, itertools

def list_cams(pattern="/dev/video*"):
    devs = sorted(int(p[10:]) for p in itertools.chain.from_iterable(
        [d for d in os.listdir('/dev') if d.startswith('video')]))
    return devs

cams = list_cams()                         # only what exists
readers = []
for cid in cams:
    try:
        r = iio.get_reader(
            f"<video{cid}>",
            size=(640, 480),               # ↓ shrink bandwidth
            input_params=['-input_format','mjpeg','-framerate','15'])
        readers.append(r)
    except Exception as e:
        print(f"cam{cid}: {e}")
        readers.append(None)

plt.ion()
fig, axs = plt.subplots(2, 3)
ims = [ax.imshow([[0]], vmin=0, vmax=255) for ax in axs.flat]

run = True
signal.signal(signal.SIGINT, lambda *a: globals().__setitem__('run', False))

while run:
    for i, r in enumerate(readers):
        if r is None:
            continue
        try:
            ims[i].set_data(r.get_next_data())
            axs.flat[i].set_title(f"cam {cams[i]}")
        except Exception as e:
            print(f"cam{cams[i]}: {e}")
            r.close(); readers[i] = None
    fig.canvas.draw_idle()
    plt.pause(0.001)
    time.sleep(0.05)

for r in readers:
    if r: r.close()
plt.close(fig)
