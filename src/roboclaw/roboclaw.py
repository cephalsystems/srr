import serial
import struct
import time
import threading

class Roboclaw(object):
    
    def init(self, port=None, address=0x80):
        # Create a lock for synchronizing changes to the actual
        # connection to the device.
        self._device_lock = threading.Lock()

        # Initialize the connection to the device (as initially
        # disconnected).
        with self._device_lock:
            self._port = port
            self._dev = None
            self._address = address

    @property
    def port(self):
        with self._device_lock:
            return self._port

    @port.setter
    def port(self, value):
        with self._device_lock:
            self._port = value
            self._dev = None

    @property
    def address(self):
        with self._device_lock:
            return self._address

    @port.setter
    def address(self, value):
        with self._device_lock:
            self._address = address

    #######################################
    # Commands 0 - 7 Standard Commands
    #
    # The following commands are the standard set of commands used
    # with packet mode.
    #######################################

    def drive_forward_m1(self, value):
        """
        0 - Drive Forward M1 

        Drive motor 1 forward. Valid data range is 0 - 127. A value of
        127 = full speed forward, 64 = about half speed forward and 0
        = full stop.
        """
        raise NotImplementedError()

    def drive_backward_m1(self, value):
        """
        1 - Drive Backwards M1 

        Drive motor 1 backwards. Valid data range is 0 - 127. A value
        of 127 full speed backwards, 64 = about half speed backward
        and 0 = full stop.
        """
        raise NotImplementedError()

    @property
    def main_voltage_minimum(self):
        # TODO: docstring
        raise NotImplementedError()

    @port.setter
    def main_voltage_minimum(self, value):
        # TODO: docstring
        raise NotImplementedError()

    @property
    def main_voltage_maximum(self):
        # TODO: docstring
        raise NotImplementedError()

    @port.setter
    def main_voltage_maximum(self, value):
        # TODO: docstring
        raise NotImplementedError()
    
    def drive_forward_m2(self, value):
        """
        4 - Drive Forward M2

        Drive motor 2 forward. Valid data range is 0 - 127. A value of
        127 full speed forward, 64 = about half speed forward and 0 =
        full stop.
        """
        raise NotImplementedError()

    def drive_backward_m2(self, value):
        """
        5 - Drive Backwards M2
        
        Drive motor 2 backwards. Valid data range is 0 - 127. A value
        of 127 full speed backwards, 64 = about half speed backward
        and 0 = full stop.
        """
        raise NotImplementedError()

    def drive_m1(self, value):
        """
        6 - Drive M1 (7 Bit)

        Drive motor 1 forward and reverse. Valid data range is 0 -
        127. A value of 0 = full speed reverse, 64 = qstop and 127 =
        full speed forward.
        """
        raise NotImplementedError()
    
    def drive_m2(self, value):
        """
        7 - Drive M2 (7 Bit)

        Drive motor 2 forward and reverse. Valid data range is 0 -
        127. A value of 0 = full speed reverse, 64 = stop and 127 =
        full speed forward.
        """
        raise NotImplementedError()

    #######################################
    # Commands 8 - 13 Mix Mode Commands
    #
    # The following commands are mix mode commands and used to control
    # speed and turn. Before a command is executed valid drive and
    # turn data is required. You only need to send both data packets
    # once. After receiving both valid drive and turn data RoboClaw
    # will begin to operate. At this point you only need to update
    # turn or drive data.
    #######################################
    
    def drive_forward(self, value):
        """
        8 - Drive Forward
        
        Drive forward in mix mode. Valid data range is 0 - 127. A
        value of 0 = full stop and 127 = full forward.
        """
        raise NotImplementedError()

    def drive_backwards(self, value):
        """
        9 - Drive Backwards

        Drive backwards in mix mode. Valid data range is 0 - 127. A
        value of 0 = full stop and 127 = full reverse.
        """
        raise NotImplementedError()

    def turn_right(self, value):
        """
        10 - Turn right

        Turn right in mix mode. Valid data range is 0 - 127. A value
        of 0 = stop turn and 127 = full speed turn. (Note that this
        assumes left motor is M1 and right is M2.)
        """
        raise NotImplementedError()

    def turn_left(self, value):
        """
        11 - Turn left

        Turn left in mix mode. Valid data range is 0 - 127. A value of
        0 = stop turn and 127 = full speed turn.
        """
        raise NotImplementedError()

    def drive_forward_backward(self, value):
        """
        12 - Drive Forward or Backward (7 Bit)

        Drive forward or backwards. Valid data range is 0 - 127. A
        value of 0 = full backward, 64 = stop and 127 = full forward.
        """
        raise NotImplementedError()

    def turn_left_right(self, value):
        """
        13 - Turn Left or Right (7 Bit)
        
        Turn left or right. Valid data range is 0 - 127. A value of 0
        = full left, 0 = stop turn and 127 = full right.
        """
        raise NotImplementedError()


checksum = 0


def sendcommand(address, command):
    global checksum
    checksum = address
    port.write(chr(address))
    checksum += command
    port.write(chr(command))
    return


def readbyte():
    global checksum
    val = struct.unpack('>B', port.read(1))
    checksum += val[0]
    return val[0]


def readsbyte():
    global checksum
    val = struct.unpack('>b', port.read(1))
    checksum += val[0]
    return val[0]


def readword():
    global checksum
    val = struct.unpack('>H', port.read(2))
    checksum += (val[0] & 0xFF)
    checksum += (val[0] >> 8) & 0xFF
    return val[0]


def readsword():
    global checksum
    val = struct.unpack('>h', port.read(2))
    checksum += val[0]
    checksum += (val[0] >> 8) & 0xFF
    return val[0]


def readlong():
    global checksum
    val = struct.unpack('>L', port.read(4))
    checksum += val[0]
    checksum += (val[0] >> 8) & 0xFF
    checksum += (val[0] >> 16) & 0xFF
    checksum += (val[0] >> 24) & 0xFF
    return val[0]


def readslong():
    global checksum
    val = struct.unpack('>l', port.read(4))
    checksum += val[0]
    checksum += (val[0] >> 8) & 0xFF
    checksum += (val[0] >> 16) & 0xFF
    checksum += (val[0] >> 24) & 0xFF
    return val[0]


def writebyte(val):
    global checksum
    checksum += val
    return port.write(struct.pack('>B', val))


def writesbyte(val):
    global checksum
    checksum += val
    return port.write(struct.pack('>b', val))


def writeword(val):
    global checksum
    checksum += val
    checksum += (val >> 8) & 0xFF
    return port.write(struct.pack('>H', val))


def writesword(val):
    global checksum
    checksum += val
    checksum += (val >> 8) & 0xFF
    return port.write(struct.pack('>h', val))


def writelong(val):
    global checksum
    checksum += val
    checksum += (val >> 8) & 0xFF
    checksum += (val >> 16) & 0xFF
    checksum += (val >> 24) & 0xFF
    return port.write(struct.pack('>L', val))


def writeslong(val):
    global checksum
    checksum += val
    checksum += (val >> 8) & 0xFF
    checksum += (val >> 16) & 0xFF
    checksum += (val >> 24) & 0xFF
    return port.write(struct.pack('>l', val))


def M1Forward(val):
    sendcommand(128, 0)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def M1Backward(val):
    sendcommand(128, 1)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def SetMinMainBattery(val):
    sendcommand(128, 2)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def SetMaxMainBattery(val):
    sendcommand(128, 3)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def M2Forward(val):
    sendcommand(128, 4)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def M2Backward(val):
    sendcommand(128, 5)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def DriveM1(val):
    sendcommand(128, 6)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def DriveM2(val):
    sendcommand(128, 7)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def ForwardMixed(val):
    sendcommand(128, 8)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def BackwardMixed(val):
    sendcommand(128, 9)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def RightMixed(val):
    sendcommand(128, 10)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def LeftMixed(val):
    sendcommand(128, 11)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def DriveMixed(val):
    sendcommand(128, 12)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def TurnMixed(val):
    sendcommand(128, 13)
    writebyte(val)
    writebyte(checksum & 0x7F)
    return


def readM1encoder():
    sendcommand(128, 16)
    enc = readslong()
    status = readbyte()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (enc, status)
    return (-1, -1)


def readM2encoder():
    sendcommand(128, 17)
    enc = readslong()
    status = readbyte()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (enc, status)
    return (-1, -1)


def readM1speed():
    sendcommand(128, 18)
    enc = readslong()
    status = readbyte()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (enc, status)
    return (-1, -1)


def readM2speed():
    sendcommand(128, 19)
    enc = readslong()
    status = readbyte()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (enc, status)
    return (-1, -1)


def ResetEncoderCnts():
    sendcommand(128, 20)
    writebyte(checksum & 0x7F)
    return


def readversion():
    sendcommand(128, 21)
    return port.read(32)


def readmainbattery():
    sendcommand(128, 24)
    val = readword()
    crc = checksum & 0x7F
    if crc == readbyte():
        return val
    return -1


def readlogicbattery():
    sendcommand(128, 25)
    val = readword()
    crc = checksum & 0x7F
    if crc == readbyte():
        return val
    return -1


def SetM1pidq(p, i, d, qpps):
    sendcommand(128, 28)
    writelong(d)
    writelong(p)
    writelong(i)
    writelong(qpps)
    writebyte(checksum & 0x7F)
    return


def SetM2pidq(p, i, d, qpps):
    sendcommand(128, 29)
    writelong(d)
    writelong(p)
    writelong(i)
    writelong(qpps)
    writebyte(checksum & 0x7F)
    return


def readM1instspeed():
    sendcommand(128, 30)
    enc = readslong()
    status = readbyte()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (enc, status)
    return (-1, -1)


def readM2instspeed():
    sendcommand(128, 31)
    enc = readslong()
    status = readbyte()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (enc, status)
    return (-1, -1)


def SetM1Duty(val):
    sendcommand(128, 32)
    writesword(val)
    writebyte(checksum & 0x7F)
    return


def SetM2Duty(val):
    sendcommand(128, 33)
    writesword(val)
    writebyte(checksum & 0x7F)
    return


def SetMixedDuty(m1, m2):
    sendcommand(128, 34)
    writesword(m1)
    writesword(m2)
    writebyte(checksum & 0x7F)
    return


def SetM1Speed(val):
    sendcommand(128, 35)
    writeslong(val)
    writebyte(checksum & 0x7F)
    return


def SetM2Speed(val):
    sendcommand(128, 36)
    writeslong(val)
    writebyte(checksum & 0x7F)
    return


def SetMixedSpeed(m1, m2):
    sendcommand(128, 37)
    writeslong(m1)
    writeslong(m2)
    writebyte(checksum & 0x7F)
    return


def SetM1SpeedAccel(accel, speed):
    sendcommand(128, 38)
    writelong(accel)
    writeslong(speed)
    writebyte(checksum & 0x7F)
    return


def SetM2SpeedAccel(accel, speed):
    sendcommand(128, 39)
    writelong(accel)
    writeslong(speed)
    writebyte(checksum & 0x7F)
    return


def SetMixedSpeedAccel(accel, speed1, speed2):
    sendcommand(128, 40)
    writelong(accel)
    writeslong(speed1)
    writeslong(speed2)
    writebyte(checksum & 0x7F)
    return


def SetM1SpeedDistance(speed, distance, buffer):
    sendcommand(128, 41)
    writeslong(speed)
    writelong(distance)
    writebyte(buffer)
    writebyte(checksum & 0x7F)
    return


def SetM2SpeedDistance(speed, distance, buffer):
    sendcommand(128, 42)
    writeslong(speed)
    writelong(distance)
    writebyte(buffer)
    writebyte(checksum & 0x7F)
    return


def SetMixedSpeedDistance(speed1, distance1, speed2, distance2, buffer):
    sendcommand(128, 43)
    writeslong(speed1)
    writelong(distance1)
    writeslong(speed2)
    writelong(distance2)
    writebyte(buffer)
    writebyte(checksum & 0x7F)
    return


def SetM1SpeedAccelDistance(accel, speed, distance, buffer):
    sendcommand(128, 44)
    writelong(accel)
    writeslong(speed)
    writelong(distance)
    writebyte(buffer)
    writebyte(checksum & 0x7F)
    return


def SetM2SpeedAccelDistance(accel, speed, distance, buffer):
    sendcommand(128, 45)
    writelong(accel)
    writeslong(speed)
    writelong(distance)
    writebyte(buffer)
    writebyte(checksum & 0x7F)
    return


def SetMixedSpeedAccelDistance(accel, speed1, distance1, speed2, distance2, buffer):
    sendcommand(128, 46)
    writelong(accel)
    writeslong(speed1)
    writelong(distance1)
    writeslong(speed2)
    writelong(distance2)
    writebyte(buffer)
    writebyte(checksum & 0x7F)
    return


def readbuffercnts():
    sendcommand(128, 47)
    buffer1 = readbyte()
    buffer2 = readbyte()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (buffer1, buffer2)
    return (-1, -1)


def readcurrents():
    sendcommand(128, 49)
    motor1 = readword()
    motor2 = readword()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (motor1, motor2)
    return (-1, -1)


def SetMixedSpeedIAccel(accel1, speed1, accel2, speed2):
    sendcommand(128, 50)
    writelong(accel1)
    writeslong(speed1)
    writelong(accel2)
    writeslong(speed2)
    writebyte(checksum & 0x7F)
    return


def SetMixedSpeedIAccelDistance(accel1, speed1, distance1, accel2, speed2, distance2, buffer):
    sendcommand(128, 51)
    writelong(accel1)
    writeslong(speed1)
    writelong(distance1)
    writelong(accel2)
    writeslong(speed2)
    writelong(distance2)
    writebyte(buffer)
    writebyte(checksum & 0x7F)
    return


def SetM1DutyAccel(accel, duty):
    sendcommand(128, 52)
    writesword(duty)
    writeword(accel)
    writebyte(checksum & 0x7F)
    return


def SetM2DutyAccel(accel, duty):
    sendcommand(128, 53)
    writesword(duty)
    writeword(accel)
    writebyte(checksum & 0x7F)
    return


def SetMixedDutyAccel(accel1, duty1, accel2, duty2):
    sendcommand(128, 54)
    writesword(duty1)
    writeword(accel1)
    writesword(duty2)
    writeword(accel2)
    writebyte(checksum & 0x7F)
    return


def readM1pidq():
    sendcommand(128, 55)
    p = readlong()
    i = readlong()
    d = readlong()
    qpps = readlong()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (p, i, d, qpps)
    return (-1, -1, -1, -1)


def readM2pidq():
    sendcommand(128, 56)
    p = readlong()
    i = readlong()
    d = readlong()
    qpps = readlong()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (p, i, d, qpps)
    return (-1, -1, -1, -1)


def readmainbatterysettings():
    sendcommand(128, 59)
    min = readword()
    max = readword()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (min, max)
    return (-1, -1)


def readlogicbatterysettings():
    sendcommand(128, 60)
    min = readword()
    max = readword()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (min, max)
    return (-1, -1)


def SetM1PositionConstants(kp, ki, kd, kimax, deadzone, min, max):
    sendcommand(128, 61)
    writelong(kd)
    writelong(kp)
    writelong(ki)
    writelong(kimax)
    writelong(min)
    writelong(max)
    return


def SetM2PositionConstants(kp, ki, kd, kimax, deadzone, min, max):
    sendcommand(128, 62)
    writelong(kd)
    writelong(kp)
    writelong(ki)
    writelong(kimax)
    writelong(min)
    writelong(max)
    return


def readM1PositionConstants():
    sendcommand(128, 63)
    p = readlong()
    i = readlong()
    d = readlong()
    imax = readlong()
    deadzone = readlong()
    min = readlong()
    max = readlong()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (p, i, d, imax, deadzone, min, max)
    return (-1, -1, -1, -1, -1, -1, -1)


def readM2PositionConstants():
    sendcommand(128, 64)
    p = readlong()
    i = readlong()
    d = readlong()
    imax = readlong()
    deadzone = readlong()
    min = readlong()
    max = readlong()
    crc = checksum & 0x7F
    if crc == readbyte():
        return (p, i, d, imax, deadzone, min, max)
    return (-1, -1, -1, -1, -1, -1, -1)


def SetM1SpeedAccelDeccelPosition(accel, speed, deccel, position, buffer):
    sendcommand(128, 65)
    writelong(accel)
    writelong(speed)
    writelong(deccel)
    writelong(position)
    writebyte(buffer)
    writebyte(checksum & 0x7F)
    return


def SetM2SpeedAccelDeccelPosition(accel, speed, deccel, position, buffer):
    sendcommand(128, 66)
    writelong(accel)
    writelong(speed)
    writelong(deccel)
    writelong(position)
    writebyte(buffer)
    writebyte(checksum & 0x7F)
    return


def SetMixedSpeedAccelDeccelPosition(accel1, speed1, deccel1, position1, accel2, speed2, deccel2, position2, buffer):
    sendcommand(128, 67)
    writelong(accel1)
    writelong(speed1)
    writelong(deccel1)
    writelong(position1)
    writelong(accel2)
    writelong(speed2)
    writelong(deccel2)
    writelong(position2)
    writebyte(buffer)
    writebyte(checksum & 0x7F)
    return


def readtemperature():
    sendcommand(128, 82)
    val = readword()
    crc = checksum & 0x7F
    if crc == readbyte():
        return val
    return -1


def readerrorstate():
    sendcommand(128, 90)
    val = readbyte()
    crc = checksum & 0x7F
    if crc == readbyte():
        return val
    return -1
