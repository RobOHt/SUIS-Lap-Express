from recordVideo import get_frame, WIDTH
import io
import time
import threading
import picamera
from PIL import Image
import numpy as np


class ImageProcessor(threading.Thread):
    def __init__(self, owner):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.owner = owner
        self.start()

    def run(self):
        # This method runs in a separate thread
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)
                    # Read the image and do some processing on it
                    raw_image = np.array(Image.open(self.stream))
                    try:
                        _, direction_choice = get_frame(raw_image)
                        print(direction_choice)
                        self.owner.direction = direction_choice
                    except:
                        pass
                    # ...
                    # ...
                    # Set done to True if you want the script to terminate
                    # at some point
                    # self.owner.done=True
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the available pool
                    with self.owner.lock:
                        self.owner.pool.append(self)


class ProcessOutput(object):
    def __init__(self):
        self.img = np.array([[1,0], [0,1]])
        self.direction = None
        self.done = False
        # Construct a pool of 4 image processors along with a lock
        # to control access between threads
        self.lock = threading.Lock()
        self.pool = [ImageProcessor(self) for i in range(4)]
        self.processor = None

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame; set the current processor going and grab
            # a spare one
            if self.processor:
                self.processor.event.set()
            with self.lock:
                if self.pool:
                    self.processor = self.pool.pop()
                else:
                    # No processor's available, we'll have to skip
                    # this frame; you may want to print a warning
                    # here to see whether you hit this case
                    self.processor = None
        if self.processor:
            self.processor.stream.write(buf)

    def flush(self):
        # When told to flush (this indicates end of recording), shut
        # down in an orderly fashion. First, add the current processor
        # back to the pool
        if self.processor:
            with self.lock:
                self.pool.append(self.processor)
                self.processor = None
        # Now, empty the pool, joining each thread as we go
        while True:
            with self.lock:
                try:
                    proc = self.pool.pop()
                except IndexError:
                    pass  # pool is empty
            proc.terminated = True
            proc.join()


def self_driving():
    with picamera.PiCamera(resolution=(WIDTH, WIDTH)) as camera:
        camera.rotation = 180
        time.sleep(2)
        output = ProcessOutput()
        camera.start_recording(output, format='mjpeg')
        while not output.done:
            print("applied")
            camera.wait_recording(0.05)
        camera.stop_recording()


if __name__ == "__main__":
    self_driving()
