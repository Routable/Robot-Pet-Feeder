from picamera import PiCamera
from time import sleep

# Initialize Camera

  
def get_video_feed():
  camera = PiCamera()
  camera.start_preview()
  camera.capture('static/image.jpg')
  camera.close()