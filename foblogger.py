import threading
import time
from pyfob import Fob


class FobLogger(threading.Thread):
    def __init__(self, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.fob = Fob()

    def run(self):
        global coordinate
        while True:
            time.sleep(0.01)
            self.lock.acquire()
            coordinate = self.fob.getcord()
            self.lock.release()
