import glob
import math
import os
import sys
import random
import time
import numpy as np
import cv2

IMAGE_SIZE_X = 98  # 640
IMAGE_SIZE_Y = 98  # 480

SHOW_PREVIEW = False

# INIT
try:
    sys.path.append(glob.glob('/opt/carla-simulator/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla


class CarEnv:
    SHOW_CAM = SHOW_PREVIEW
    SECONDS_PER_EPISODE = int(input("How long would you like this car to run?"))

    im_width = IMAGE_SIZE_X
    im_height = IMAGE_SIZE_Y
    front_cam = None

    def __init__(self):
        # Connect
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()

        # Grab blueprint
        self.blueprint_library = self.world.get_blueprint_library()

        # Create training data file
        self.data_size = 100005
        time_stamp = str(int(time.time()))[-5:]
        if input("Creating new dataset? ") == "yes":
            self.file_name = f"training_data-SIZE{self.data_size}-TIME{time_stamp}.npy"
            self.training_data = []
        else:
            self.file_name = input("Which file to continue from? ")
            self.training_data = list(np.load(self.file_name, allow_pickle=True))

    def reset(self):
        self.collision_list = []
        self.actor_list = []

        # -------------------------------Create a Tesla model3 car
        self.model3 = self.blueprint_library.filter('model3')[0]
        transform = random.choice(self.world.get_map().get_spawn_points())
        self.vehicle = self.world.spawn_actor(self.model3, transform)
        self.vehicle.set_autopilot(True)
        self.actor_list.append(self.vehicle)
        print(f'created {self.vehicle.type_id}')

        # -------------------------------Create an rgb camera and attach it onto the car
        self.cam_rgb = self.blueprint_library.find('sensor.camera.rgb')
        self.cam_rgb.set_attribute("image_size_x", f"{self.im_width}")
        self.cam_rgb.set_attribute("image_size_y", f"{self.im_height}")
        self.cam_rgb.set_attribute("fov", "110")
        transform = carla.Transform(carla.Location(x=2.5, z=0.7))
        self.sensor = self.world.spawn_actor(self.cam_rgb, transform, attach_to=self.vehicle)
        self.actor_list.append(self.sensor)
        print(f'created {self.sensor.type_id}')

        # -------------------------------Wait 4 seconds to compensate for car dropping time & sensor wait time
        count_down = 30
        for i in range(count_down):
            print(f"t-{count_down - i}")
            if count_down - i == 5:
                print("Ignition sequence start!")
            time.sleep(1)

        # ------------------------------- episode has started
        print("lift off!")
        self.sensor.listen(lambda data: self.record_data(data))

        time.sleep(self.SECONDS_PER_EPISODE)
        self.exit_data_collection()
        return self.front_cam

    def record_data(self, image):
        # -----------------Cheat that disables traffic lights:
        if self.vehicle.is_at_traffic_light():
            traffic_light = self.vehicle.get_traffic_light()
            if traffic_light.get_state() == carla.TrafficLightState.Red:
                traffic_light.set_state(carla.TrafficLightState.Green)

        # ------------------------------------------------------------------------Process steering data
        control = self.vehicle.get_control()
        steer = round(control.steer, 2)
        steer = 0.0 if steer == -0.0 else steer

        # ------------------------------------------------------------------------Process imagery data
        i = np.array(image.raw_data)
        i2 = i.reshape((self.im_height, self.im_width, 4))  # rgba
        irgb = i2[:, :, :3]  # rgb, alpha removed
        igray = cv2.cvtColor(irgb, cv2.COLOR_RGB2GRAY)
        if self.SHOW_CAM:
            # Save the image to disk. For visualising data.
            try:
                os.mkdir("./output")
            except FileExistsError:
                pass
            cv2.imwrite(f"output/{image.frame}.png", igray)

        # ------------------------------------------------------------------------Save image and steering to a np file.
        self.training_data.append([igray, steer])

        if len(self.training_data) % 1000 == 0:
            print(len(self.training_data))
            np.save(self.file_name, self.training_data)
        if len(self.training_data) == self.data_size:
            # self.exit_data_collection()
            pass

    def exit_data_collection(self):
        for actor in self.actor_list:
            actor.destroy()
            print(f"destroyed {actor.type_id}")
        exit()


if __name__ == "__main__":
    Car = CarEnv()
    Car.reset()
