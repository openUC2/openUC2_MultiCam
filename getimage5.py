import imageio as iio
import matplotlib.pyplot as plt

myCameras = [2,4,6,8,10,12]
myDevices = []
for iCamera in myCameras:
  camera = iio.get_reader("<video"+str(iCamera)+">")
  myDevices.append(camera)

for camera in myDevices:
  screenshot = camera.get_data(0)
  print(screenshot)

for camera in myDevices:
  camera.close()

  
  #plt.imshow(screenshot)
  #plt.show()
