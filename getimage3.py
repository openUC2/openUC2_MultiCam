import imageio as iio
import matplotlib.pyplot as plt

myCameras = [2,4,6,8,10,12]
for iCamera in myCameras:
#  camera = iio.get_reader("<video2>")
  camera = iio.get_reader("<video"+str(iCamera)+">")
  screenshot = camera.get_data(0)
  camera.close()

  print(screenshot)
  plt.imshow(screenshot)
  plt.show()
