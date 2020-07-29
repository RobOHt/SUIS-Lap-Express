from DCRotation import VehicleControl
from recordVideo import record_video, WIDTH
from rapidCaptureTest import ProcessOutput
import threading
import time
import math
import picamera


direction = -10


def sharp_apply_direction():
    print("!!!!!!!!!!!!!!!!!!!!!!!!DIRECTION APPLIED!!!!!!!!!!!!!!!!!!!!!!!!")
    frame_rate = 0.2
    vehicle = VehicleControl()
    vehicle.reset()
    turn_int = 0.5
    global direction
    if direction == -1:  # Turn left
        vehicle.turn_left()
        time.sleep(0.05)
        vehicle.reset()
        time.sleep(frame_rate)
    elif direction == 1:  # Turn right
        vehicle.turn_right()
        time.sleep(0.05)
        vehicle.reset()
        time.sleep(frame_rate)
    elif direction == 0:  # Forward
        vehicle.forward()
        time.sleep(0.1)
        vehicle.reset()
        time.sleep(frame_rate)
    elif direction == -10:  # Stop
        vehicle.reset()
    

def sharp_show_direction(direction=1):
    if direction == 0:
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    elif direction == -1:
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    elif direction == 1:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    elif direction == -2:
        print("<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-")
    elif direction == 2:
        print("->->->->->->->->->->->->->->->->->->->->->->->->->->")
    elif direction == -10:
        print("STOP")


def sharp_steering_wheel():
    global direction
    vehicle = VehicleControl()
    vehicle.reset()

    while True:
        sharp_show_direction(direction)
        direction = input("Which direction to steer? Use W, A, S, D")
        if direction == "a":
            direction = -1
        elif direction == "d":
            direction = 1
        elif direction == "q":
            direction = -2
        elif direction == "e":
            direction = 2
        elif direction == "s":
            direction = -10
            vehicle.reset()
        else:
            direction = 0
        sharp_apply_direction()
            
            
def self_driving(): 
    with picamera.PiCamera(resolution=(WIDTH, WIDTH)) as camera:
        camera.rotation = 180
        time.sleep(2)
        output = ProcessOutput()
        camera.start_recording(output, format='mjpeg')
        while not output.done:
            global direction
            print(output.direction)
            direction = output.direction
            sharp_apply_direction()
            camera.wait_recording(0.5)
        camera.stop_recording()


def enable_control():
    vehicle = VehicleControl()

    burnTime = int(input("How long do you want me to run?"))
    timer = threading.Thread(target=vehicle.auto_reset, args=[burnTime])
    steer = threading.Thread(target=sharp_steering_wheel)
    #applier = threading.Thread(target=sharp_apply_direction)
    driver = threading.Thread(target=self_driving)
    # camera = threading.Thread(target=record_video)

    steer.start()
    #applier.start()
    timer.start()
    driver.start()
    # camera.start()
    steer.join()
    #applier.join()
    timer.join()
    driver.join()
    # camera.join()


enable_control()
