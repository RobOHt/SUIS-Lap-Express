from DCRotation import VehicleControl
import threading


def show_direction(direction=1):
    if direction == 1:
        print("----------------------------------------------------")
    elif direction == 0:
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    elif direction == 2:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


def steering_wheel():
    vehicle = VehicleControl()
    vehicle.reset()
    vehicle.forward()

    direction = 1
    while True:
        show_direction(direction)
        direction = input("Which direction to steer? Use W, A, S, D")
        if direction == "a":
            direction = 0
        elif direction == "d":
            direction = 2
        elif direction == "s":
            vehicle.reset()
        else:
            direction = 1

        if direction == 0:
            vehicle.turn_left()
        elif direction == 2:
            vehicle.turn_right()
        elif direction == 1:
            vehicle.forward()


def enable_control():
    vehicle = VehicleControl()
    burnTime = int(input("How long do you want me to run?"))
    timer = threading.Thread(target=vehicle.auto_reset, args=[burnTime])
    steer = threading.Thread(target=steering_wheel)

    steer.start()
    timer.start()
    steer.join()
    timer.join()


enable_control()
