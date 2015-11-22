from ctypes import *


class PARAM(Structure):
    _fields_ = [('nSenseDegree', c_short),
                ('nHightFre', c_short),
                ('nTimeConstant', c_short),
                ('nWorkFre', c_short),
                ('nModeOfSign', c_short),
                ('nGateOfJam', c_short),
                ('nHold1', c_short),
                ('nHold2', c_short)]


class DEVICEINFO(Structure):
    _fields_ = [('nRouteNum', c_short),
                ('nType', c_short),
                ('nDeviceID', c_short),
                ('nSwitchNo', c_short)]


class Symtop(object):
    '''
    Class that connects to Symtop EEG amplifier by wrapping the SDK dynamic link library
    '''

    def __init__(self):
        self.channels = 8;
        self.EEGAMP = WinDLL('EEGAMP.dll')
        self.connected = False

    def connect(self):
        self.data_handler = self.EEGAMP.OpenDevice()
        self.connected = True

    def geteeg(self):
        if not self.connected:
            self.connect()
        nCounts = c_ulong()

        while True:
            data = (c_short * 90)()
            self.EEGAMP.ReadData(self.data_handler, byref(data), byref(nCounts))
            n = nCounts.value
            if not n:
                continue
            return data


if __name__ == '__main__':
    symtop = Symtop()
    while True:
        data = symtop.acquire()
