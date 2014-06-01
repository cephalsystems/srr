import serial
import struct
import time
import threading

class Roboclaw(object):
    """
    Interface for controlling Orion Roboclaw motor controllers.
    """
    
    def __init__(self, port=None, address=0x80):
        # Create a lock for synchronizing changes to the actual
        # connection to the device.
        self._device_lock = threading.Lock()

        # Initialize the connection to the device (as initially
        # disconnected).
        with self._device_lock:
            self._device = serial.Serial(port=None, timeout=0.250)
            self._port = port
            self._address = address
            self._checksum = 0

    @property
    def port(self):
        with self._device_lock:
            return self._port

    @property
    def is_connected(self):
        with self._device_lock:            
            return (self._device.port is None)

    @port.setter
    def port(self, value):
        with self._device_lock:
            self._device.close()
            self._device.port = None
            self._port = value

    @property
    def address(self):
        with self._device_lock:
            return self._address

    @address.setter
    def address(self, value):
        with self._device_lock:
            self._address = address

    #######################################
    # Commands 0 - 7 Standard Commands
    #
    # The following commands are the standard set of commands used
    # with packet mode.
    #######################################

    def m1_forward(self, value):
        """
        0 - Drive Forward M1 

        Drive motor 1 forward. Valid data range is 0 - 127. A value of
        127 = full speed forward, 64 = about half speed forward and 0
        = full stop.
        """
        with self._device_lock:
            self._send_command(0)
            self._write_byte(value)
            self._write_checksum()

    def m1_backward(self, value):
        """
        1 - Drive Backwards M1 

        Drive motor 1 backwards. Valid data range is 0 - 127. A value
        of 127 full speed backwards, 64 = about half speed backward
        and 0 = full stop.
        """
        with self._device_lock:
            self._send_command(1)
            self._write_byte(value)
            self._write_checksum()

    def set_main_voltage_minimum(self, voltage):
        """
        2 - Set Minimum Main Voltage

        Sets main battery (B- / B+) minimum voltage level. If the battery
        voltages drops below the set voltage level RoboClaw will shut
        down. The value is cleared at start up and must set after each
        power up. The voltage is set in .2 volt increments. A value of 0
        sets the minimum value allowed which is 6V. The valid data range
        is 6.0 - 30.0 (volts).
        """
        # The formula for calculating the voltage is:
        # (Desired Volts - 6) x 5 = Value
        value = round((voltage - 6) * 5)

        with self._device_lock:
            self._send_command(2)
            self._write_byte(value)
            self._write_checksum()

    def set_main_voltage_maximum(self, voltage):
        """
        3 - Set Maximum Main Voltage

        Sets main battery (B- / B+) maximum voltage level. The valid data
        range is 0 - 30 (volts). If you are using a battery of any type 
        you can ignore this setting. During regenerative breaking a back
        voltage is applied to charge the battery. When using an ATX type
        power supply if it senses anything over 16V it will shut
        down. By setting the maximum voltage level, RoboClaw before
        exceeding it will go into hard breaking mode until the voltage
        drops below the maximum value set.
        """
        # The formula for calculating the voltage is:
        # Desired Volts x 5.12 = Value
        value = round(voltage * 5.12)

        with self._device_lock:
            self._send_command(3)
            self._write_byte(value)
            self._write_checksum()
        
    def m2_forward(self, value):
        """
        4 - Drive Forward M2

        Drive motor 2 forward. Valid data range is 0 - 127. A value of
        127 full speed forward, 64 = about half speed forward and 0 =
        full stop.
        """
        with self._device_lock:
            self._send_command(4)
            self._write_byte(value)
            self._write_checksum()

    def m2_backward(self, value):
        """
        5 - Drive Backwards M2
        
        Drive motor 2 backwards. Valid data range is 0 - 127. A value
        of 127 full speed backwards, 64 = about half speed backward
        and 0 = full stop.
        """
        with self._device_lock:
            self._send_command(5)
            self._write_byte(value)
            self._write_checksum()

    def m1_drive(self, value):
        """
        6 - Drive M1 (7 Bit)

        Drive motor 1 forward and reverse. Valid data range is 0 -
        127. A value of 0 = full speed reverse, 64 = qstop and 127 =
        full speed forward.
        """
        with self._device_lock:
            self._send_command(6)
            self._write_byte(value)
            self._write_checksum()
    
    def m2_drive(self, value):
        """
        7 - Drive M2 (7 Bit)

        Drive motor 2 forward and reverse. Valid data range is 0 -
        127. A value of 0 = full speed reverse, 64 = stop and 127 =
        full speed forward.
        """
        with self._device_lock:
            self._send_command(7)
            self._write_byte(value)
            self._write_checksum()

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
    
    def mixed_forward(self, value):
        """
        8 - Drive Forward
        
        Drive forward in mix mode. Valid data range is 0 - 127. A
        value of 0 = full stop and 127 = full forward.
        """
        with self._device_lock:
            self._send_command(8)
            self._write_byte(value)
            self._write_checksum()

    def mixed_backward(self, value):
        """
        9 - Drive Backwards

        Drive backwards in mix mode. Valid data range is 0 - 127. A
        value of 0 = full stop and 127 = full reverse.
        """
        with self._device_lock:
            self._send_command(9)
            self._write_byte(value)
            self._write_checksum()

    def mixed_right(self, value):
        """
        10 - Turn right

        Turn right in mix mode. Valid data range is 0 - 127. A value
        of 0 = stop turn and 127 = full speed turn. (Note that this
        assumes left motor is M1 and right is M2.)
        """
        with self._device_lock:
            self._send_command(10)
            self._write_byte(value)
            self._write_checksum()

    def mixed_left(self, value):
        """
        11 - Turn left

        Turn left in mix mode. Valid data range is 0 - 127. A value of
        0 = stop turn and 127 = full speed turn. (Note that this
        assumes left motor is M1 and right is M2.)
        """
        with self._device_lock:
            self._send_command(11)
            self._write_byte(value)
            self._write_checksum()

    def mixed_drive(self, value):
        """
        12 - Drive Forward or Backward (7 Bit)

        Drive forward or backwards. Valid data range is 0 - 127. A
        value of 0 = full backward, 64 = stop and 127 = full forward.
        """
        with self._device_lock:
            self._send_command(12)
            self._write_byte(value)
            self._write_checksum()

    def mixed_turn(self, value):
        """
        13 - Turn Left or Right (7 Bit)
        
        Turn left or right. Valid data range is 0 - 127. A value of 0
        = full left, 0 = stop turn and 127 = full right. (Note that this
        assumes left motor is M1 and right is M2.)
        """
        with self._device_lock:
            self._send_command(13)
            self._write_byte(value)
            self._write_checksum()

    #######################################                                           
    # Version, Status, and Settings Commands
    #
    # The following commands are used to read board status, version
    # information and set configuration values.
    ####################################### 

    @property
    def firmware_version(self):
        """
        RoboClaw firmware version. 

        Returns up to 32 bytes and is terminated by a null character.

        Uses:
        21 - Read Firmware Version
        """
        with self._device_lock:
            self._send_command(21)
            return self._read(32)

    @property
    def main_voltage(self):
        """
        The main battery voltage level connected to B+ and B- terminals (in volts).

        Uses:
        24 - Read Main Battery Voltage Level
        """
        with self._device_lock:
            self._send_command(24)
            val = self._read_word() * 0.1
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return val
            else:
                raise ValueError("Checksum mismatch.")

    @property
    def logic_voltage(self):
        """
        The logic battery voltage level connected to LB+ and LB- terminals (in volts).
        
        Uses:
        25 - Read Logic Battery Voltage Level
        """
        with self._device_lock:
            self._send_command(25)
            val = self._read_word() * 0.1
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return val
            else:
                raise ValueError("Checksum mismatch.")
    
    def set_logic_voltage_minimum(self, value):
        """
        26 - Set Minimum Logic Voltage Level
        
        Sets logic input (LB- / LB+) minimum voltage level. If the
        battery voltages drops below the set voltage level RoboClaw
        will shut down. The value is cleared at start up and must set
        after each power up. The valid data range is 6.0 - 28.0 (volts).
        """
        raise NotImplementedError()

    def set_logic_voltage_maximum(self, value):
        """
        27 - Set Maximum Logic Voltage Level
        
        Sets logic input (LB- / LB+) maximum voltage level. The valid
        data range is 0.0 - 28.0 (volts). By setting the maximum
        voltage level RoboClaw will go into shut down and requires a
        hard reset to recovers.
        """
        raise NotImplementedError()
    
    @property
    def motor_currents(self):
        """
        The current draw from each motor (in amps).
        
        Uses:
        49 - Read Motor Currents
        """
        with self._device_lock:
            self._send_command(49);
            motor1 = self._read_word() * 0.010
            motor2 = self._read_word() * 0.010
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (motor1, motor2)
            else:
                raise ValueError("Checksum mismatch.")

    @property
    def m1_velocity_pid(self):
        """
        The velocity PID and QPPS settings for M1.

        Several motor and quadrature combinations can be used with
        RoboClaw. In some cases the default PID values will need to be
        tuned for the systems being driven. This gives greater
        flexibility in what motor and encoder combinations can be
        used. The RoboClaw PID system consist of four constants
        starting with QPPS, P = Proportional, I= Integral and D=
        Derivative. The defaults values are:

        QPPS = 44000 
        P = 0x00010000 
        I = 0x00008000 
        D = 0x00004000

        QPPS is the speed of the encoder when the motor is at 100% power.

        Uses:
        55 - Read Motor 1 Velocity P, I, D Constants
        28 - Set Velocity PID Constants for M1
        """
        with self._device_lock:
            self._send_command(55)
            p = self._read_long()
            i = self._read_long()
            d = self._read_long()
            qpps = self._read_long()
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (p,i,d,qpps)
            else:
                raise ValueError("Checksum mismatch.")

    @property
    def m2_velocity_pid(self):
        """
        The velocity PID and QPPS settings for M2.

        Several motor and quadrature combinations can be used with
        RoboClaw. In some cases the default PID values will need to be
        tuned for the systems being driven. This gives greater
        flexibility in what motor and encoder combinations can be
        used. The RoboClaw PID system consist of four constants
        starting with QPPS, P = Proportional, I= Integral and D=
        Derivative. The defaults values are:

        QPPS = 44000 
        P = 0x00010000 
        I = 0x00008000 
        D = 0x00004000

        QPPS is the speed of the encoder when the motor is at 100% power.
        
        Uses:
        56 - Read Motor 2 Velocity P, I, D Constants
        29 - Set Velocity PID Constants for M2.
        """
        with self._device_lock:
            self._send_command(56)
            p = self._read_long()
            i = self._read_long()
            d = self._read_long()
            qpps = self._read_long()
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (p,i,d,qpps)
            else:
                raise ValueError("Checksum mismatch.")

    @property
    def main_voltage_range(self):
        """
        The Main Battery Voltages cutoffs, (min, max) in volts.
        
        Uses:
        59 - Read Main Battery Voltage Settings
        57 - Set Main Battery Voltages
        """
        with self._device_lock:
            self._send_command(59)
            min = self._read_word() * 0.1
            max = self._read_word() * 0.1
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (min, max)
            else:
                raise ValueError("Checksum mismatch.")

    @property
    def logic_voltage_range(self):
        """
        The Logic Battery Voltages cutoffs, (min, max) in volts.
        
        Uses:
        60 - Read Logic Battery Voltage Settings
        58 - Set Logic Battery Voltages
        """
        with self._device_lock:
            self._send_command(60)
            min = self._read_word() * 0.1
            max = self._read_word() * 0.1
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (min, max)
            else:
                raise ValueError("Checksum mismatch.")

    @main_voltage_range.setter
    def main_voltage_range(self, value):
        """
        57 - Set Main Battery Voltages

        Set the Main Battery Voltages cutoffs, Min and Max.
        """
        # TODO: What are the units here?
        raise NotImplementedError()

    @logic_voltage_range.setter
    def logic_voltage_range(self, value):
        """
        58 - Set Logic Battery Voltages

        Set the Logic Battery Voltages cutoffs, Min and Max.
        """
        # TODO: What are the units here?
        raise NotImplementedError()
    
    @property
    def m1_position_pid(self):
        """
        The position PID settings for M1.

        Uses:
        63 - Read Motor 1 Position P, I, D Constants
        """
        with self._device_lock:
            self._send_command(63)
            p = self._read_long()
            i = self._read_long()
            d = self._read_long()
            imax = self._read_long()
            deadzone = self._read_long()
            min = self._read_long()
            max = self._read_long()
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (p,i,d,imax,deadzone,min,max)
            else:
                raise ValueError("Checksum mismatch.")

    @property
    def m2_position_pid(self):
        """
        The position PID settings for M2.
        
        Uses:
        64 - Read Motor 2 Position P, I, D Constants
        """
        with self._device_lock:
            self._send_command(64)
            p = self._read_long()
            i = self._read_long()
            d = self._read_long()
            imax = self._read_long()
            deadzone = self._read_long()
            min = self._read_long()
            max = self._read_long()
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (p,i,d,imax,deadzone,min,max)
            else:
                raise ValueError("Checksum mismatch.")
        
    @property
    def temperature(self):
        """
        The board temperature. Value returned is in degrees Celsius.

        Uses:
        82 - Read Temperature
        """
        with self._device_lock:
            self._send_command(82);
            val = self._read_word() * 0.1
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return val
            else:
                raise ValueError("Checksum mismatch.")

    @property
    def error_status(self):
        """
        The current error status.

        Error Mask
        ----------
        Normal             0x00
        M1 OverCurrent     0x01
        M2 OverCurrent     0x02
        E-Stop             0x04
        Temperature        0x08
        Main Battery High  0x10
        Main Battery Low   0x20
        Logic Battery High 0x40
        Logic Battery Low  0x80
        """
        with self._device_lock:
            self._send_command(90);
            val = self._read_byte()
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return val
            else:
                raise ValueError("Checksum mismatch.")

    @property
    def m1_encoder_mode(self):
        """
        The encoder mode for M1.

        Encoder Mode bits
        -----------------
        Bit 7    Enable RC/Analog Encoder support
        Bit 6-1  N/A
        Bit 0    Quadrature(0)/Absolute(1)
        
        Uses:
        91 - Read Encoder Mode
        92 - Set Motor 1 Encoder Mode
        """
        raise NotImplementedError()

    @property
    def m2_encoder_mode(self):
        """
        The encoder mode for M2.

        Encoder Mode bits
        -----------------
        Bit 7    Enable RC/Analog Encoder support
        Bit 6-1  N/A
        Bit 0    Quadrature(0)/Absolute(1)
        
        Uses:
        91 - Read Encoder Mode
        93 - Set Motor 2 Encoder Mode
        """
        raise NotImplementedError()

    @m1_encoder_mode.setter
    def m1_encoder_mode(self, value):
        """
        92 - Set Motor 1 Encoder Mode
        
        Set the Encoder Mode for motor 1.
        """
        raise NotImplementedError()

    @m2_encoder_mode.setter
    def m2_encoder_mode(self, value):
        """
        93 - Set Motor 2 Encoder Mode

        Set the Encoder Mode for motor 1.
        """
        raise NotImplementedError()

    def write_settings(self):
        """
        94 - Write Settings to EEPROM
        
        Writes all settings to non-volatile memory.
        """
        raise NotImplementedError()

    ####################################### 
    # Quadrature Encoder Commands
    #
    # The following commands are used in dealing with the quadrature
    # decoding counter registers. The quadrature decoder is a simple
    # counter that counts the incoming pulses, tracks the direction
    # and speed of each pulse. There are two registers one each for M1
    # and M2. (Note: A microcontroller with a hardware UART is
    # recommended for use with packet serial modes).
    #######################################     

    @property
    def m1_encoder(self):
        """
        Tuple of decoder M1 counter and status.
        
        Counter is a long variable which represents the current count
        which can be any value from 0 - 4,294,967,295. Each pulse from
        the quadrature encoder will increment or decrement the counter
        depending on the direction of rotation.
        
        Status is the status byte for M1 decoder. It tracks counter
        underflow, direction, overflow and if the encoder is
        operational. The byte value represents:
        
        Bit0 - Counter Underflow (1= Underflow Occurred, Clear After Reading)
        Bit1 - Direction (0 = Forward, 1 = Backwards)
        Bit2 - Counter Overflow (1= Underflow Occurred, Clear After Reading)
        Bit3 - Reserved
        Bit4 - Reserved
        Bit5 - Reserved
        Bit6 - Reserved
        Bit7 - Reserved
        
        Uses:
        16 - Read Quadrature Encoder Register M1
        """
        with self._device_lock:
            self._send_command(16)
            enc = self._read_slong()
            status = self._read_byte()
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (enc, status)
            else:
                raise ValueError("Checksum mismatch.")

    @property
    def m2_encoder(self):
        """
        Tuple of decoder M2 counter and status.
        
        Counter is a long variable which represents the current count
        which can be any value from 0 - 4,294,967,295. Each pulse from
        the quadrature encoder will increment or decrement the counter
        depending on the direction of rotation.
        
        Status is the status byte for M2 decoder. It tracks counter
        underflow, direction, overflow and if the encoder is
        operational. The byte value represents:
        
        Bit0 - Counter Underflow (1= Underflow Occurred, Clear After Reading)
        Bit1 - Direction (0 = Forward, 1 = Backwards)
        Bit2 - Counter Overflow (1= Underflow Occurred, Clear After Reading)
        Bit3 - Reserved
        Bit4 - Reserved
        Bit5 - Reserved
        Bit6 - Reserved
        Bit7 - Reserved
        
        Uses:
        17 - Read Quadrature Encoder Register M2
        """
        with self._device_lock:
            self._send_command(17)
            enc = self._read_slong()
            status = self._read_byte()
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (enc,status)
            else:
                raise ValueError("Checksum mismatch.")

    @property
    def m1_counter_speed(self):
        """
        M1 counter speed and direction. Returned value is in pulses per
        second. RoboClaw keeps track of how many pulses received per
        second for both decoder channels.

        Uses:
        18 - Read Speed M1
        """
        with self._device_lock:
            self._send_command(18)
            enc = self._read_slong()
            status = self._read_byte()
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (enc, direction)
            else:
                raise ValueError("Checksum mismatch.")

    @property
    def m2_counter_speed(self):
        """
        M2 counter speed and direction. Returned value is in pulses per
        second. RoboClaw keeps track of how many pulses received per
        second for both decoder channels.

        Uses:
        19 - Read Speed M2
        """
        with self._device_lock:
            self._send_command(19)
            enc = self._read_slong()
            status = self._read_byte()
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (enc, direction)
            else:
                raise ValueError("Checksum mismatch.")
    
    def reset_encoders(self):
        """
        20 - Reset Quadrature Encoder Counters

        Will reset both quadrature decoder counters to zero.
        """
        with self._device_lock:
            self._send_command(20)
            self._write_checksum()

    ####################################### 
    # Advanced Motor Control
    #
    # The following commands are used to control motor speeds,
    # acceleration and distance using the quadrature encoders. All
    # speeds are given in quad pulses per second (QPPS) unless
    # otherwise stated. Quadrature encoders of different types and
    # manufactures can be used. However many have different
    # resolutions and maximum speeds at which they operate. So each
    # quadrature encoder will produce a different range of pulses per
    # second.
    #######################################     
    
    @m1_velocity_pid.setter
    def m1_velocity_pid(self, p_i_d_qpps):
        """
        28 - Set PID Constants M1

        Several motor and quadrature combinations can be used with
        RoboClaw. In some cases the default PID values will need to be
        tuned for the systems being driven. This gives greater
        flexibility in what motor and encoder combinations can be
        used. The RoboClaw PID system consist of four constants
        starting with QPPS, P = Proportional, I= Integral and D=
        Derivative. The defaults values are:

        QPPS = 44000 
        P = 0x00010000 = 65536
        I = 0x00008000 = 32768
        D = 0x00004000 = 16384

        QPPS is the speed of the encoder when the motor is at 100% power.
        """
        p, i, d, qpps = p_i_d_qpps
        
        with self._device_lock:
            self._send_command(28)
            self._write_long(d)
            self._write_long(p)
            self._write_long(i)
            self._write_long(qpps)
            self._write_checksum();

    @m2_velocity_pid.setter
    def m2_velocity_pid(self, p_i_d_qpps):
        """
        29 - Set PID Constants M2

        Several motor and quadrature combinations can be used with
        RoboClaw. In some cases the default PID values will need to be
        tuned for the systems being driven. This gives greater
        flexibility in what motor and encoder combinations can be
        used. The RoboClaw PID system consist of four constants
        starting with QPPS, P = Proportional, I= Integral and D=
        Derivative. The defaults values are:

        QPPS = 44000
        P = 0x00010000 = 65535
        I = 0x00008000 = 32768
        D = 0x00004000 = 16384
        
        QPPS is the speed of the encoder when the motor is at 100%
        power. P, I, D are the default values used after a reset.
        """
        p, i, d, qpps = p_i_d_qpps
        
        with self._device_lock:
            self._send_command(29)
            self._write_long(d)
            self._write_long(p)
            self._write_long(i)
            self._write_long(qpps)
            self._write_checksum();
    
    @property
    def m1_current_speed(self):
        """
        The current pulse per 125th of a second. This is a high
        resolution version of m1_counter_speed(). It can be used to
        make a independent PID routine. The resolution of the command
        is required to create a PID routine using any microcontroller
        or PC used to drive RoboClaw.
        
        Uses:
        30 - Read Current Speed M1        
        """
        with self._device_lock:
            self._send_command(30)
            enc = self._read_slong()
            status = self._read_byte()
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (enc, status)
            else:
                raise ValueError("Checksum mismatch.")

    @property
    def m2_current_speed(self):
        """
        The current pulse per 125th of a second. This is a high
        resolution version of m2_counter_speed(). It can be used to
        make a independent PID routine. The resolution of the command
        is required to create a PID routine using any microcontroller
        or PC used to drive RoboClaw.
        
        Uses:
        31 - Read Current Speed M1        
        """
        with self._device_lock:
            self._send_command(31)
            enc = self._read_slong()
            status = self._read_byte()
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (enc, status)
            else:
                raise ValueError("Checksum mismatch.")

    def m1_set_duty(self, value):
        """
        32 - Drive M1 With Signed Duty Cycle

        Drive M1 using a duty cycle value. The duty cycle is used to
        control the speed of the motor without a quadrature
        encoder. The duty value is signed and the range is +/-1500.
        """
        with self._device_lock:
            self._send_command(32)
            self._write_sword(value)
            self._write_checksum()

    def m2_set_duty(self, value):
        """
        33 - Drive M2 With Signed Duty Cycle

        Drive M2 using a duty cycle value. The duty cycle is used to
        control the speed of the motor without a quadrature
        encoder. The duty value is signed and the range is +/-1500.
        """
        with self._device_lock:
            self._send_command(33)
            self._write_sword(value)
            self._write_checksum()

    def mixed_set_duty(self, value_m1, value_m2):
        """
        34 - Mix Mode Drive M1 / M2 With Signed Duty Cycle

        Drive both M1 and M2 using a duty cycle value. The duty cycle
        is used to control the speed of the motor without a quadrature
        encoder. The duty value is signed and the range is +-1500.
        """
        with self._device_lock:
            self._send_command(34)
            self._write_sword(value_m1)
            self._write_sword(value_m2)
            self._write_checksum()

    def m1_set_speed(self, speed):
        """
        35 - Drive M1 With Signed Speed

        Drive M1 using a speed value. The sign indicates which
        direction the motor will turn. This command is used to drive
        the motor by quad pulses per second. Different quadrature
        encoders will have different rates at which they generate the
        incoming pulses. The values used will differ from one encoder
        to another. Once a value is sent the motor will begin to
        accelerate as fast as possible until the defined rate is
        reached.
        """
        with self._device_lock:
            self._send_command(35)
            self._write_slong(speed)
            self._write_checksum()

    def m2_set_speed(self, speed):
        """
        36 - Drive M2 With Signed Speed

        Drive M2 using a speed value. The sign indicates which
        direction the motor will turn. This command is used to drive
        the motor by quad pulses per second. Different quadrature
        encoders will have different rates at which they generate the
        incoming pulses. The values used will differ from one encoder
        to another. Once a value is sent the motor will begin to
        accelerate as fast as possible until the defined rate is
        reached.
        """
        with self._device_lock:
            self._send_command(36)
            self._write_slong(speed)
            self._write_checksum();

    def mixed_set_speed(self, speed_m1, speed_m2):
        """
        37 - Mix Mode Drive M1 / M2 With Signed Speed

        Drive M1 and M2 in the same command using a signed speed
        value. The sign indicates which direction the motor will
        turn. This command is used to drive both motors by quad pulses
        per second. Different quadrature encoders will have different
        rates at which they generate the incoming pulses. The values
        used will differ from one encoder to another. Once a value is
        sent the motor will begin to accelerate as fast as possible
        until the rate defined is reached.
        """
        with self._device_lock:
            self._send_command(37)
            self._write_slong(speed_m1)
            self._write_slong(speed_m2)
            self._write_checksum()

    def m1_set_speed_accel(self, speed, accel):
        """
        38 - Drive M1 With Signed Speed And Acceleration

        Drive M1 with a signed speed and acceleration value. The sign
        indicates which direction the motor will run. The acceleration
        values are not signed. This command is used to drive the motor
        by quad pulses per second and using an acceleration value for
        ramping. Different quadrature encoders will have different
        rates at which they generate the incoming pulses. The values
        used will differ from one encoder to another. Once a value is
        sent the motor will begin to accelerate incrementally until
        the rate defined is reached.

        Quadrature encoders send 4 pulses per tick. So 1000 ticks
        would be counted as 4000 pulses. The acceleration is measured
        in speed per second. An acceleration value of 12,000 QPPS with
        a speed of 12,000 QPPS would accelerate a motor from 0 to
        12,000 QPPS in 1 second. Another example would be an
        acceleration value of 24,000 QPPS and a speed value of 12,000
        QPPS would accelerate the motor to 12,000 QPPS in 0.5 seconds.
        """
        with self._device_lock:
            self._send_command(38)
            self._write_long(accel)
            self._write_slong(speed)
            self._write_checksum()

    def m2_set_speed_accel(self, speed, accel):
        """
        39 - Drive M2 With Signed Speed And Acceleration

        Drive M2 with a signed speed and acceleration value. The sign
        indicates which direction the motor will run. The acceleration
        value is not signed. This command is used to drive the motor
        by quad pulses per second and using an acceleration value for
        ramping. Different quadrature encoders will have different
        rates at which they generate the incoming pulses. The values
        used will differ from one encoder to another. Once a value is
        sent the motor will begin to accelerate incrementally until
        the rate defined is reached.

        Quadrature encoders send 4 pulses per tick. So 1000 ticks
        would be counted as 4000 pulses. The acceleration is measured
        in speed per second. An acceleration value of 12,000 QPPS with
        a speed of 12,000 QPPS would accelerate a motor from 0 to
        12,000 QPPS in 1 second. Another example would be an
        acceleration value of 24,000 QPPS and a speed value of 12,000
        QPPS would accelerate the motor to 12,000 QPPS in 0.5 seconds.
        """
        with self._device_lock:
            self._send_command(39)
            self._write_long(accel)
            self._write_slong(speed)
            self._write_checksum()

    def mixed_set_speed_accel(self, accel, speed_m1, speed_m2):
        """
        40 - Mix Mode Drive M1 / M2 With Signed Speed And Acceleration

        Drive M1 and M2 in the same command using one value for
        acceleration and two signed speed values for each motor. The
        sign indicates which direction the motor will run. The
        acceleration value is not signed. The motors are sync during
        acceleration. This command is used to drive the motor by quad
        pulses per second and using an acceleration value for
        ramping. Different quadrature encoders will have different
        rates at which they generate the incoming pulses. The values
        used will differ from one encoder to another. Once a value is
        sent the motor will begin to accelerate incrementally until
        the rate defined is reached.

        Quadrature encoders send 4 pulses per tick. So 1000 ticks
        would be counted as 4000 pulses. The acceleration is measured
        in speed per second. An acceleration value of 12,000 QPPS with
        a speed of 12,000 QPPS would accelerate a motor from 0 to
        12,000 QPPS in 1 second. Another example would be an
        acceleration value of 24,000 QPPS and a speed value of 12,000
        QPPS would accelerate the motor to 12,000 QPPS in 0.5 seconds.
        """
        with self._device_lock:
            self._send_command(40)
            self._write_long(accel)
            self._write_slong(speed_m1)
            self._write_slong(speed_m2)
            self._write_checksum()

    def m1_set_speed_distance(self, speed, distance, buffered=False):
        """
        41 - Buffered M1 Drive With Signed Speed And Distance

        Drive M1 with a signed speed and distance value. The sign
        indicates which direction the motor will run. The distance
        value is not signed. This command is buffered. This command is
        used to control the top speed and total distance traveled by
        the motor. Each motor channel M1 and M2 has separate
        buffers. This command will execute immediately if no other
        command for that channel is executing, otherwise the command
        will be buffered in the order it was sent. Any buffered or
        executing command can be stopped when a new command is issued
        by setting the Buffer argument. All values used are in quad
        pulses per second.

        The buffered argument can be set to True or False. If a value
        of 0 is used the command will be buffered and executed in the
        order sent. If a value of 1 is used the current running
        command is stopped, any other commands in the buffer are
        deleted and the new command is executed.
        """
        with self._device_lock:
            self._send_command(41)
            self._write_slong(speed)
            self._write_long(distance)
            self._write_byte(buffered)
            self._write_checksum()

    def m2_set_speed_distance(self, speed, distance, buffered=False):
        """
        42 - Buffered M2 Drive With Signed Speed And Distance

        Drive M2 with a signed speed and distance value. The sign
        indicates which direction the motor will run. The distance
        value is not signed. This command is buffered. This command is
        used to control the top speed and total distance traveled by
        the motor. Each motor channel M1 and M2 has separate
        buffers. This command will execute immediately if no other
        command for that channel is executing, otherwise the command
        will be buffered in the order it was sent. Any buffered or
        executing command can be stopped when a new command is issued
        by setting the Buffer argument. All values used are in quad
        pulses per second.

        The buffered argument can be set to True or False. If a value
        of 0 is used the command will be buffered and executed in the
        order sent. If a value of 1 is used the current running
        command is stopped, any other commands in the buffer are
        deleted and the new command is executed.
        """
        with self._device_lock:
            self._send_command(42)
            self._write_slong(speed)
            self._write_long(distance)
            self._write_byte(buffered)
            self._write_checksum()

    def mixed_set_speed_distance(self, speed_m1, distance_m1, speed_m2, distance_m2, buffered=False):
        """
        43 - Buffered Mix Mode Drive M1 / M2 With Signed Speed And Distance

        Drive M1 and M2 with a speed and distance value. The sign
        indicates which direction the motor will run. The distance
        value is not signed. This command is buffered. Each motor
        channel M1 and M2 have separate buffers. This command will
        execute immediately if no other command for that channel is
        executing, otherwise the command will be buffered in the order
        it was sent. Any buffered or executing command can be stopped
        when a new command is issued by setting the Buffer
        argument. All values used are in quad pulses per second.

        The buffered argument can be set to True or False. If a value
        of 0 is used the command will be buffered and executed in the
        order sent. If a value of 1 is used the current running
        command is stopped, any other commands in the buffer are
        deleted and the new command is executed.
        """
        with self._device_lock:
            self._send_command(43)
            self._write_slong(speed_m1)
            self._write_long(distance_m1)
            self._write_slong(speed_m2)
            self._write_long(distance_m2)
            self._write_byte(buffered)
            self._write_checksum()

    def m1_set_speed_accel_distance(self, speed, accel, distance, buffered=False):
        """
        44 - Buffered M1 Drive With Signed Speed, Accel And Distance

        Drive M1 with a speed, acceleration and distance value. The
        sign indicates which direction the motor will run. The
        acceleration and distance values are not signed. This command
        is used to control the motor's top speed, total distanced
        traveled and at what incremental acceleration value to use
        until the top speed is reached. Each motor channel M1 and M2
        have separate buffers. This command will execute immediately
        if no other command for that channel is executing, otherwise
        the command will be buffered in the order it was sent. Any
        buffered or executing command can be stopped when a new
        command is issued by setting the Buffer argument. All values
        used are in quad pulses per second.

        The buffered argument can be set to True or False. If a value
        of 0 is used the command will be buffered and executed in the
        order sent. If a value of 1 is used the current running
        command is stopped, any other commands in the buffer are
        deleted and the new command is executed.
        """
        with self._device_lock:
            self._send_command(44)
            self._write_long(accel)
            self._write_slong(speed)
            self._write_long(distance)
            self._write_byte(buffer)
            self._write_checksum()

    def m2_set_speed_accel_distance(self, speed, accel, distance, buffered=False):
        """
        45 - Buffered M2 Drive With Signed Speed, Accel And Distance

        Drive M2 with a speed, acceleration and distance value. The
        sign indicates which direction the motor will run. The
        acceleration and distance values are not signed. This command
        is used to control the motors top speed, total distanced
        traveled and at what incremental acceleration value to use
        until the top speed is reached. Each motor channel M1 and M2
        have separate buffers. This command will execute immediately
        if no other command for that channel is executing, otherwise
        the command will be buffered in the order it was sent. Any
        buffered or executing command can be stopped when a new
        command is issued by setting the Buffer argument. All values
        used are in quad pulses per second.

        The buffered argument can be set to True or False. If a value
        of 0 is used the command will be buffered and executed in the
        order sent. If a value of 1 is used the current running
        command is stopped, any other commands in the buffer are
        deleted and the new command is executed.
        """
        with self._device_lock:
            self._send_command(45)
            self._write_long(accel)
            self._write_slong(speed)
            self._write_long(distance)
            self._write_byte(buffer)
            self._write_checksum()

    def mixed_set_speed_accel_distance(self, accel, speed_m1, distance_m1, speed_m2, distance_m2, buffered=False):
        """
        46 - Buffered Mix Mode Drive M1 / M2 With Signed Speed, Accel And Distance

        Drive M1 and M2 with a speed, acceleration and distance
        value. The sign indicates which direction the motor will
        run. The acceleration and distance values are not signed. This
        command is used to control both motors top speed, total
        distanced traveled and at what incremental acceleration value
        to use until the top speed is reached. Each motor channel M1
        and M2 have separate buffers. This command will execute
        immediately if no other command for that channel is executing,
        otherwise the command will be buffered in the order it was
        sent. Any buffered or executing command can be stopped when a
        new command is issued by setting the Buffer argument. All
        values used are in quad pulses per second.

        The buffered argument can be set to True or False. If a value
        of 0 is used the command will be buffered and executed in the
        order sent. If a value of 1 is used the current running
        command is stopped, any other commands in the buffer are
        deleted and the new command is executed.
        """
        with self._device_lock:
            self._send_command(46)
            self._write_long(accel)
            self._write_slong(speed_m1)
            self._write_long(distance_m1)
            self._write_slong(speed_m2)
            self._write_long(distance_m2)
            self._write_byte(buffered)
            self._write_checksum()

    @property
    def buffer_length(self):
        """
        Motor M1 and M2 buffer lengths. This can be used to determine how many
        commands are waiting to execute.

        The return values represent how many commands per buffer are
        waiting to be executed. The maximum buffer size per motor is
        31 commands. A return value of 0x80(128) indicates the buffer
        is empty. A return value of 0 indiciates the last command sent
        is executing. A value of 0x80 indicates the last command
        buffered has finished.

        Uses:
        47 - Read Buffer Length
        """
        with self._device_lock:
            self._send_command(47);
            buffer1 = self._read_byte();
            buffer2 = self._read_byte();
            crc = self._checksum & 0x7F
            if crc == self._read_byte():
                return (buffer1,buffer2);
            else:
                raise ValueError("Checksum mismatch.")
            
    def mixed_set_speed_iaccels(self, accel_m1, speed_m1, accel_m2, speed_m2):
        """
        50 - Mix Mode Drive M1 / M2 With Signed Speed And Individual Accelerations

        Drive M1 and M2 in the same command using one value for
        acceleration and two signed speed values for each motor. The
        sign indicates which direction the motor will run. The
        acceleration value is not signed. The motors are sync during
        acceleration. This command is used to drive the motor by quad
        pulses per second and using an acceleration value for
        ramping. Different quadrature encoders will have different
        rates at which they generate the incoming pulses. The values
        used will differ from one encoder to another.

        Quadrature encoders send 4 pulses per tick. So 1000 ticks
        would be counted as 4000 pulses. The acceleration is measured
        in speed per second. An acceleration value of 12,000 QPPS with
        a speed of 12,000 QPPS would accelerate a motor from 0 to
        12,000 QPPS in 1 second. Another example would be an
        acceleration value of 24,000 QPPS and a speed value of 12,000
        QPPS would accelerate the motor to 12,000 QPPS in 0.5 seconds
        """
        with self._device_lock:
            self._send_command(50)
            self._write_long(accel_m1)
            self._write_slong(speed_m1)
            self._write_long(accel_m2)
            self._write_slong(speed_m2)
            self._write_checksum()

    def mixed_set_speed_iaccel_distance(self, accel_m1, speed_m1, distance_m1, accel_m2, speed_m2, distance_m2, buffered=False):
        """
        51 - Buffered Mix Mode Drive M1 / M2 With Signed Speed, Individual Accel And Distance
        
        Drive M1 and M2 with a speed, acceleration and distance
        value. The sign indicates which direction the motor will
        run. The acceleration and distance values are not signed. This
        command is used to control both motors top speed, total
        distanced traveled and at what incremental acceleration value
        to use until the top speed is reached. Each motor channel M1
        and M2 have separate buffers. This command will execute
        immediately if no other command for that channel is executing,
        otherwise the command will be buffered in the order it was
        sent. Any buffered or executing command can be stopped when
        a new command is issued by setting the Buffer argument. All
        values used are in quad pulses per second.

        The buffered argument can be set to True or False. If a value
        of 0 is used the command will be buffered and executed in the
        order sent. If a value of 1 is used the current running
        command is stopped, any other commands in the buffer are
        deleted and the new command is executed.
        """
        with self._device_lock:
            self._send_command(51)
            self._write_long(accel_m1)
            self._write_slong(speed_m1)
            self._write_long(distance_m1)
            self._write_long(accel_m2)
            self._write_slong(speed_m2)
            self._write_long(distance_m2)
            self._write_byte(buffered)
            self._write_checksum()

    def m1_set_duty_accel(self, accel, duty):
        """
        52 - Drive M1 With Signed Duty And Acceleration

        Drive M1 with a signed duty and acceleration value. The sign
        indicates which direction the motor will run. The acceleration
        values are not signed. This command is used to drive the motor
        by PWM and using an acceleration value for ramping. Accel is
        the rate per second at which the duty changes from the current
        duty to the specified duty.

        The duty value is signed and the range is +/-1500.
        The accel value range is 0 to 65535.
        """
        with self._device_lock:
            self._send_command(52)
            self._write_sword(duty)
            self._write_word(accel)
            self._write_checksum()
    
    def m2_set_duty_accel(self, accel, duty):
        """
        53 - Drive M2 With Signed Duty And Acceleration
        
        Drive M2 with a signed duty and acceleration value. The sign
        indicates which direction the motor will run. The acceleration
        values are not signed. This command is used to drive the motor
        by PWM and using an acceleration value for ramping. Accel is
        the rate per second at which the duty changes from the current
        duty to the specified duty.

        The duty value is signed and the range is +/-1500.
        The accel value range is 0 to 65535.
        """
        with self._device_lock:
            self._send_command(53)
            self._write_sword(duty)
            self._write_word(accel)
            self._write_checksum()

    def mixed_set_duty_accel(self, accel_m1, duty_m1, accel_m2, duty_m2):
        """
        Drive M1 and M2 in the same command using acceleration and
        duty values for each motor. The sign indicates which direction
        the motor will run. The acceleration value is not signed. This
        command is used to drive the motor by PWM using an
        acceleration value for ramping.
        
        The duty value is signed and the range is +/-1500.
        The accel value range is 0 to 65535.
        """
        with self._device_lock:
            self._send_command(54)
            self._write_sword(duty_m1)
            self._write_word(accel_m1)
            self._write_sword(duty_m2)
            self._write_word(accel_m2)
            self._write_checksum()

    @m1_position_pid.setter
    def m1_position_pid(self, p_i_d_imax_dz_min_max):
        """
        The RoboClaw Position PID system consist of seven constants
        starting with P = Proportional, I= Integral and D= Derivative,
        MaxI = Maximum Integral windup, Deadzone in encoder counts,
        MinPos = Minimum Position and MaxPos = Maximum Position. The
        defaults values are all zero.

        Position constants are used only with the Position commands,
        65,66 and 67 and RC or Analog mode when in absolute mode with
        encoders or potentiometers.

        Uses:
        61 - Set Motor 1 Position PID Constants
        63 - Read Motor 1 Position P, I, D Constants
        """
        p,i,d,imax,deadzone,min,max = p_i_d_imax_dz_min_max
        
        with self._device_lock:
            self._send_command(61)
            self._write_long(p)
            self._write_long(i)
            self._write_long(d)
            self._write_long(imax)
            self._write_long(deadzone)
            self._write_long(min);
            self._write_long(max);

    @m2_position_pid.setter
    def m2_position_pid(self, value):
        """
        The RoboClaw Position PID system consist of seven constants
        starting with P = Proportional, I= Integral and D= Derivative,
        MaxI = Maximum Integral windup, Deadzone in encoder counts,
        MinPos = Minimum Position and MaxPos = Maximum Position. The
        defaults values are all zero.

        Position constants are used only with the Position commands,
        65,66 and 67 and RC or Analog mode when in absolute mode with
        encoders or potentiometers.

        Uses:
        62 - Set Motor 2 Position PID Constants
        64 - Read Motor 2 Position P, I, D Constants
        """
        p,i,d,imax,deadzone,min,max = p_i_d_imax_dz_min_max
        
        with self._device_lock:
            self._send_command(62)
            self._write_long(p)
            self._write_long(i)
            self._write_long(d)
            self._write_long(imax)
            self._write_long(deadzone)
            self._write_long(min);
            self._write_long(max);

    def m1_set_speed_accel_decel_position(self, accel, speed, decel, position):
        """
        65 - Drive M1 with signed Speed, Accel, Deccel and Position

        Move M1 position from the current position to the specified
        new position and hold the new position. Accel sets the
        acceleration value and deccel the decceleration value. QSpeed
        sets the speed in quadrature pulses the motor will run at
        after acceleration and before decceleration.
        """
        with self._device_lock:
            self._send_command(65)
            self._write_long(accel)
            self._write_long(speed)
            self._write_long(deccel)
            self._write_long(position)
            self._write_byte(buffer)
            self._write_checksum()

    def m2_set_speed_accel_decel_position(self, accel, speed, decel, position):
        """
        66 - Drive M2 with signed Speed, Accel, Deccel and Position

        Move M2 position from the current position to the specified
        new position and hold the new position. Accel sets the
        acceleration value and deccel the decceleration value. QSpeed
        sets the speed in quadrature pulses the motor will run at
        after acceleration and before decceleration.
        """
        with self._device_lock:
            self._send_command(66)
            self._write_long(accel)
            self._write_long(speed)
            self._write_long(deccel)
            self._write_long(position)
            self._write_byte(buffer)
            self._write_checksum()
        
    def mixed_set_speed_accel_decel_position(self, accel_m1, speed_m1, decel_m1, position_m1, accel_m2, speed_m2, decel_m2, position_m2, buffered=False):
        """
        67 - Drive M1 & M2 with signed Speed, Accel, Deccel and Position

        Move M1 & M2 positions from their current positions to the
        specified new positions and hold the new positions. Accel sets
        the acceleration value and deccel the decceleration
        value. QSpeed sets the speed in quadrature pulses the motor
        will run at after acceleration and before decceleration.
        """
        with self._device_lock:
            self._send_command(67)
            self._write_long(accel1)
            self._write_long(speed1)
            self._write_long(deccel1)
            self._write_long(position1)
            self._write_long(accel2)
            self._write_long(speed2)
            self._write_long(deccel2)
            self._write_long(position2)
            self._write_byte(buffer)
            self._write_checksum()

    def _write(self, value):
        try:
            if self._device.port is None:
                self._device.port = self._port
                self._device.open()
            return self._device.write(value)
        except serial.SerialException:
            self._device.close()
            self._device.port = None
            return 0

    def _read(self, length):
        try:
            if self._device.port is None:
                self._device.port = self._port
                self._device.open()
            return self._device.read(length)
        except serial.SerialException:
            self._device.close()
            self._device.port = None
            return chr(0) * length

    def _send_command(self, command):
        self._checksum = self._address
        self._write(chr(self._address))
        self._checksum += command
        self._write(chr(command))
        
    def _read_byte(self):
        val = struct.unpack('>B', self._read(1))
        self._checksum += val[0]
        return val[0]
        
    def _read_sbyte(self):
        val = struct.unpack('>b', self._read(1))
        self._checksum += val[0]
        return val[0]

    def _read_word(self):
        val = struct.unpack('>H', self._read(2))
        self._checksum += (val[0] & 0xFF)
        self._checksum += (val[0] >> 8) & 0xFF
        return val[0]

    def _read_sword(self):
        val = struct.unpack('>h', self._read(2))
        self._checksum += val[0]
        self._checksum += (val[0] >> 8) & 0xFF
        return val[0]

    def _read_long(self):
        val = struct.unpack('>L', self._read(4))
        self._checksum += val[0]
        self._checksum += (val[0] >> 8) & 0xFF
        self._checksum += (val[0] >> 16) & 0xFF
        self._checksum += (val[0] >> 24) & 0xFF
        return val[0]

    def _read_slong(self):
        val = struct.unpack('>l', self._read(4))
        self._checksum += val[0]
        self._checksum += (val[0] >> 8) & 0xFF
        self._checksum += (val[0] >> 16) & 0xFF
        self._checksum += (val[0] >> 24) & 0xFF
        return val[0]
        
    def _write_byte(self, val):
        val = int(val)
        self._checksum += val
        return self._write(struct.pack('>B', val))

    def _write_sbyte(self, val):
        val = int(val)
        self._checksum += val
        return self._write(struct.pack('>b', val))

    def _write_word(self, val):
        val = int(val)
        self._checksum += val
        self._checksum += (val >> 8) & 0xFF
        return self._write(struct.pack('>H', val))

    def _write_sword(self, val):
        val = int(val)
        self._checksum += val
        self._checksum += (val >> 8) & 0xFF
        return self._write(struct.pack('>h', val))
        
    def _write_long(self, val):
        val = int(val)
        self._checksum += val
        self._checksum += (val >> 8) & 0xFF
        self._checksum += (val >> 16) & 0xFF
        self._checksum += (val >> 24) & 0xFF
        return self._write(struct.pack('>L', val))

    def _write_slong(self, val):
        val = int(val)
        self._checksum += val
        self._checksum += (val >> 8) & 0xFF
        self._checksum += (val >> 16) & 0xFF
        self._checksum += (val >> 24) & 0xFF
        return self._write(struct.pack('>l', val))

    def _write_checksum(self):
        return self._write_byte(self._checksum & 0x7F);
        
