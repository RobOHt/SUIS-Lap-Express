import RPi.GPIO as GPIO
import time


class VehicleControl:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        self.Motor1A = 33
        self.Motor1B = 35
        self.Motor1E = 37

        self.Motor2A = 24
        self.Motor2B = 5
        self.Motor2E = 26

    def forward(self, motor=None):
        if motor == "A":
            GPIO.setup(self.Motor1A, GPIO.OUT)
            GPIO.setup(self.Motor1B, GPIO.OUT)
            GPIO.setup(self.Motor1E, GPIO.OUT)

            print("Turning motor 1 ON")

            GPIO.output(self.Motor1A, GPIO.HIGH)
            GPIO.output(self.Motor1B, GPIO.LOW)
            GPIO.output(self.Motor1E, GPIO.HIGH)

        elif motor == "B":
            GPIO.setup(self.Motor2A, GPIO.OUT)
            GPIO.setup(self.Motor2B, GPIO.OUT)
            GPIO.setup(self.Motor2E, GPIO.OUT)

            print("Turning motor 2 ON")

            GPIO.output(self.Motor2A, GPIO.LOW)
            GPIO.output(self.Motor2B, GPIO.HIGH)
            GPIO.output(self.Motor2E, GPIO.HIGH)

        elif motor is None:
            GPIO.setup(self.Motor1A, GPIO.OUT)
            GPIO.setup(self.Motor1B, GPIO.OUT)
            GPIO.setup(self.Motor1E, GPIO.OUT)

            print("Turning motor 1 ON")

            GPIO.output(self.Motor1A, GPIO.HIGH)
            GPIO.output(self.Motor1B, GPIO.LOW)
            GPIO.output(self.Motor1E, GPIO.HIGH)

            GPIO.setup(self.Motor2A, GPIO.OUT)
            GPIO.setup(self.Motor2B, GPIO.OUT)
            GPIO.setup(self.Motor2E, GPIO.OUT)

            print("Turning motor 2 ON")

            GPIO.output(self.Motor2A, GPIO.LOW)
            GPIO.output(self.Motor2B, GPIO.HIGH)
            GPIO.output(self.Motor2E, GPIO.HIGH)

    def turn_left(self):
        self.forward()
        GPIO.output(self.Motor2E, GPIO.LOW)

    def turn_right(self):
        self.forward()
        GPIO.output(self.Motor1E, GPIO.LOW)

    def reset(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.Motor1A, GPIO.OUT)
        GPIO.setup(self.Motor1B, GPIO.OUT)
        GPIO.setup(self.Motor1E, GPIO.OUT)

        GPIO.output(self.Motor1A, GPIO.LOW)
        GPIO.output(self.Motor1B, GPIO.LOW)
        GPIO.output(self.Motor1E, GPIO.LOW)

        GPIO.setup(self.Motor2A, GPIO.OUT)
        GPIO.setup(self.Motor2B, GPIO.OUT)
        GPIO.setup(self.Motor2E, GPIO.OUT)

        GPIO.output(self.Motor2A, GPIO.LOW)
        GPIO.output(self.Motor2B, GPIO.LOW)
        GPIO.output(self.Motor2E, GPIO.LOW)

    def auto_reset(self, burnTime=60):
        time.sleep(burnTime)
        self.reset()
        exit()


Car = VehicleControl()
Car.reset()
Car.forward()
Car.reset()
