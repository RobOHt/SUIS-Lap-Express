import RPi.GPIO as GPIO
import time
#GPIO.setwarnings(False)


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
        if motor == "A" or motor is None:
            #print("motor1 start")
            GPIO.setup(self.Motor1A, GPIO.OUT)
            GPIO.setup(self.Motor1B, GPIO.OUT)
            GPIO.setup(self.Motor1E, GPIO.OUT)

            GPIO.output(self.Motor1A, GPIO.HIGH)
            GPIO.output(self.Motor1B, GPIO.LOW)
            GPIO.output(self.Motor1E, GPIO.HIGH)

        if motor == "B" or motor is None:
            #print("motor2 start")
            GPIO.setup(self.Motor2A, GPIO.OUT)
            GPIO.setup(self.Motor2B, GPIO.OUT)
            GPIO.setup(self.Motor2E, GPIO.OUT)

            GPIO.output(self.Motor2A, GPIO.LOW)
            GPIO.output(self.Motor2B, GPIO.HIGH)
            GPIO.output(self.Motor2E, GPIO.HIGH)

    def turn_left(self):
        self.forward("A")
        self.reset("B")

    def turn_right(self):
        self.forward("B")
        self.reset("A")
        
    def pincer_left(self):
        self.forward("A")
        self.back("B")
        
    def pincer_right(self):
        self.forward("B")
        self.back("A")
    
    def reset(self, motor=None):
        GPIO.setmode(GPIO.BOARD)
        
        if motor == "A" or motor is None: 
            GPIO.setup(self.Motor1A, GPIO.OUT)
            GPIO.setup(self.Motor1B, GPIO.OUT)
            GPIO.setup(self.Motor1E, GPIO.OUT)

            GPIO.output(self.Motor1A, GPIO.LOW)
            GPIO.output(self.Motor1B, GPIO.LOW)
            GPIO.output(self.Motor1E, GPIO.LOW)

        if motor == "B" or motor is None: 
            GPIO.setup(self.Motor2A, GPIO.OUT)
            GPIO.setup(self.Motor2B, GPIO.OUT)
            GPIO.setup(self.Motor2E, GPIO.OUT)

            GPIO.output(self.Motor2A, GPIO.LOW)
            GPIO.output(self.Motor2B, GPIO.LOW)
            GPIO.output(self.Motor2E, GPIO.LOW)
            
    def back(self, motor=None):
        if motor == "A" or motor is None:
            #print("motor1 start")
            GPIO.setup(self.Motor1A, GPIO.OUT)
            GPIO.setup(self.Motor1B, GPIO.OUT)
            GPIO.setup(self.Motor1E, GPIO.OUT)

            GPIO.output(self.Motor1A, GPIO.LOW)
            GPIO.output(self.Motor1B, GPIO.HIGH)
            GPIO.output(self.Motor1E, GPIO.HIGH)

        if motor == "B" or motor is None:
            #print("motor2 start")
            GPIO.setup(self.Motor2A, GPIO.OUT)
            GPIO.setup(self.Motor2B, GPIO.OUT)
            GPIO.setup(self.Motor2E, GPIO.OUT)

            GPIO.output(self.Motor2A, GPIO.HIGH)
            GPIO.output(self.Motor2B, GPIO.LOW)
            GPIO.output(self.Motor2E, GPIO.HIGH)

    def auto_reset(self, burnTime=60):
        time.sleep(burnTime)
        self.reset()
        exit()


if __name__ == "__main__": 
    for i in range(3):
        Car = VehicleControl()
        Car.reset()
        Car.pincer_right()
        time.sleep(0.5)
        Car.forward()
        time.sleep(0.1)
        Car.pincer_left()
        time.sleep(0.42)
        Car.reset()
        time.sleep(0.5)
    
