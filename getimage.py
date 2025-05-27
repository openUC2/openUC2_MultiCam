import imageio as iio
import matplotlib.pyplot as plt

camera = iio.get_reader("<video2>")
screenshot = camera.get_data(0)
camera.close()

print(screenshot)
plt.imshow(screenshot)
plt.show()
