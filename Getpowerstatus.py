from ctypes import windll, byref, Structure, Array
kernel32 = windll.kernel32

from ctypes import c_ushort, c_ubyte, c_ulong, c_char

import winsound, sys

def beep(sound):
    winsound.PlaySound('abcd.wav', winsound.SND_FILENAME)

BYTE = c_ubyte
WORD = c_ushort
DWORD = c_ulong

class DStructure(Structure):
    _abstract_ = None
    _fields_ = None # only for pychecker
    
    def dump(self, indent="", INDENT="   "):
        print "%s%s:" % (indent, self.__class__.__name__)
        for name, fmt in self._fields_:
            val = getattr(self, name)
            if isinstance(val, Structure):
                val.dump(indent + INDENT)
            elif isinstance(val, long) or isinstance(val, int):
                print "%s%30s: %s (0x%x)" % (indent, name, val, val)
            else:
                print "%s%30s: %r" % (indent, name, val)
        print

class SYSTEM_POWER_STATUS(DStructure):
    _fields_ = [("ACLineStatus", BYTE),
                ("BatteryFlag", BYTE),
                ("BatteryLifePercent", BYTE),
                ("Reserved1", BYTE),
                ("BatteryLifeTime", DWORD),
                ("BatteryFullLifeTime", DWORD)]

while __name__ == '__main__':
    sps = SYSTEM_POWER_STATUS()
    kernel32.GetSystemPowerStatus(byref(sps))
    #print sps.ACLineStatus
    #print sps.BatteryLifePercent
    while sps.ACLineStatus ==1 and sps.BatteryLifePercent==100:
        kernel32.GetSystemPowerStatus(byref(sps))
        #winsound.Beep(500,1000)
        beep(sys.argv[0])
    #sps.dump()

