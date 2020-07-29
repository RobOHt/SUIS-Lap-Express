from picamera import PiCamera
import time
import os

time_stamp = str(time.time())[-4:]
camera = PiCamera()
camera.rotation = 180

try: 
    os.mkdir("./output")
except: 
    pass

camera.start_recording(f"./output/{time_stamp}.h264")
time.sleep(7)
camera.stop_recording()
