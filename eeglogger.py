import threading
from pysymtop import Symtop


class EEGLogger(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.symtop = Symtop()

    def run(self):
        while True:
            self.symtop.geteeg()
