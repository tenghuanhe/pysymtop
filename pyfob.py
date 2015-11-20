# I should write a class for Flock of Birds
# But how?
from time import sleep

import serial

from utils import dataconvert


class Fob(object):
    def __init__(self):
        self.ser1 = serial.Serial()
        self.ser2 = serial.Serial()

        self.fs = 100
        self.all_data = (0, 0, 0, 0, 0, 0)
        # ser1 is master, and ser2 is the only slave
        # two birds are both connected to the host via RS-232
        # if only the master is connected to the host and slave
        # is connected to the master via FBB,
        # the comand sent needs changing to include FBB information
        # Since I have two RS-232 cable, I didnot trouble using FBB command
        self.ser1.port = 'COM1'
        self.ser1.baudrate = 115200
        self.ser1.open()

        self.ser2.port = 'COM4'
        self.ser2.baudrate = 115200
        self.ser2.open()

        # Hello birds
        self.ser1.setRTS(True)
        sleep(0.5)
        self.ser1.setRTS(False)
        sleep(0.5)
        self.ser2.setRTS(True)
        sleep(0.5)
        self.ser2.setRTS(False)
        sleep(0.5)

        # Could be replaced by ser.flushInput
        n = self.ser1.inWaiting()
        if n > 0:
            self.ser1.read(n)

        n = self.ser2.inWaiting()
        if n > 0:
            self.ser2.read(n)

        # auto-configure flock of birds
        self.ser1.write('P')  # command
        self.ser1.write(chr(50))  # parameter 50
        self.ser1.write(chr(2))  # number of birds
        sleep(1)

        self.ser2.write('Y')
        sleep(1)

    def getcord(self):
        self.ser2.write('B')
        while self.ser2.inWaiting() < 12:
            continue
        data = self.ser2.read(12)
        cord = dataconvert(data)
        return cord

    def close(self):
        self.ser1.close()
        self.ser2.close()


if __name__ == '__main__':
    fob = Fob()
    while True:
        fob.getcord()
