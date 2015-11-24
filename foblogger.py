import threading
import time
from pyfob import Fob
import main


class FobLogger(threading.Thread):
    def __init__(self, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.fob = Fob()

    def run(self):
        while True:
            time.sleep(0.01)
            self.lock.acquire()
            main.coordinate = self.fob.getcord()    # I hope this will work!, but now I dont have time deal with it;
            self.lock.release()
