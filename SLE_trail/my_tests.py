import glob
import os
import sys

actor_list = []
IMAGE_SIZE_X = 650  # 640
IMAGE_SIZE_Y = 480  # 480

try:
    sys.path.append(glob.glob('/opt/carla-simulator/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time
import numpy as np
import cv2


def process_img(image):
    i = np.array(image.raw_data)
    i2 = i.reshape((IMAGE_SIZE_Y, IMAGE_SIZE_X, 4))  # rgba
    irgb = i2[:, :, :3]  # rgb, alpha removed

    # cv2.imshow("frame", irgb)
    # cv2.waitKey(1)
    # return irgb/255.0

    return image.save_to_disk(f"output/{image.frame}.png")


try:
    # Connect
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    # get world and blueprint objects
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    # -------------------------------Spawn a vehicle and make it auto-pilot

    # spawn vehicle

    bp = random.choice(blueprint_library.filter('model3'))
    spawn_point = random.choice(world.get_map().get_spawn_points())
    vehicle = world.spawn_actor(bp, spawn_point)

    actor_list.append(vehicle)
    print('created %s' % vehicle.type_id)

    # -------------------------------Start manual-driving
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))

    # -------------------------------Spawn a camera
    cam_bp = blueprint_library.find('sensor.camera.rgb')
    cam_bp.set_attribute("image_size_x", f"{IMAGE_SIZE_X}")
    cam_bp.set_attribute("image_size_y", f"{IMAGE_SIZE_Y}")
    cam_bp.set_attribute("fov", "100")

    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    sensor = world.spawn_actor(cam_bp, spawn_point, attach_to=vehicle)
    actor_list.append(sensor)
    print('created %s' % sensor.type_id)

    # -------------------------------Get camera data
    sensor.listen(lambda data: process_img(data))


finally:
    time.sleep(10)
    for actor in actor_list:
        print(f"{actor.type_id} destroyed")
        actor.destroy()
    print("all actors destroyed")


