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
        raise NotImplementedError()

    @property
    def main_voltage(self):
        """
        The main battery voltage level connected to B+ and B- terminals (in volts).

        Uses:
        24 - Read Main Battery Voltage Level
        """
        raise NotImplementedError()

    @property
    def logic_voltage(self):
        """
        The logic battery voltage level connected to LB+ and LB- terminals (in volts).
        
        Uses:
        25 - Read Logic Battery Voltage Level
        """
        raise NotImplementedError()

    @logic_voltage_minimum.setter
    def logic_voltage_minimum(self, value):
        """
        26 - Set Minimum Logic Voltage Level
        
        Sets logic input (LB- / LB+) minimum voltage level. If the
        battery voltages drops below the set voltage level RoboClaw
        will shut down. The value is cleared at start up and must set
        after each power up. The valid data range is 6.0 - 28.0 (volts).
        """
        raise NotImplementedError()

    @logic_voltage_maximum.setter
    def logic_voltage_maximum(self, value):
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
        The current draw from each motor in amps.
        
        Uses:
        49 - Read Motor Currents
        """
        raise NotImplementedError()

    @property
    def m1_velocity_pidq(self):
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
        raise NotImplementedError()

    @property
    def m2_velocity_pidq(self):
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
        raise NotImplementedError()

    @main_voltage_range.setter
    def main_voltage_range(self, value):
        """
        57 - Set Main Battery Voltages

        Set the Main Battery Voltages cutoffs, Min and Max.
        """
        raise NotImplementedError()

    @logic_voltage_range.setter
    def logic_voltage_range(self, value):
        """
        58 - Set Logic Battery Voltages

        Set the Logic Battery Voltages cutoffs, Min and Max.
        """
        raise NotImplementedError()

    @property
    def main_voltage_range(self):
        """
        The Main Battery Voltages cutoffs, (min, max) in volts.
        
        Uses:
        59 - Read Main Battery Voltage Settings
        57 - Set Main Battery Voltages
        """
        raise NotImplementedError()

    @property
    def logic_voltage_range(self):
        """
        The Logic Battery Voltages cutoffs, (min, max) in volts.
        
        Uses:
        60 - Read Logic Battery Voltage Settings
        58 - Set Logic Battery Voltages
        """
        raise NotImplementedError()

    @property
    def m1_position_pid(self):
        """
        The position PID settings for M1.

        Uses:
        63 - Read Motor 1 Position P, I, D Constants
        """
        raise NotImplementedError()

    @property
    def m2_position_pid(self):
        """
        The position PID settings for M2.
        
        Uses:
        64 - Read Motor 2 Position P, I, D Constants
        """
        raise NotImplementedError()
        
    @property
    def temperature(self):
        """
        The board temperature. Value returned is in degrees Celsius.

        Uses:
        82 - Read Temperature
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        # TODO: add rest of encoder status documentation.
        """
        Decoder M1 counter and status.
        
        Uses:
        16 - Read Quadrature Encoder Register M1
        """
        raise NotImplementedError()

    @property
    def m2_encoder(self):
        # TODO: add rest of encoder status documentation.
        """
        Decoder M2 counter and status.
        
        Uses:
        17 - Read Quadrature Encoder Register M2
        """
        raise NotImplementedError()

    @property
    def m1_counter_speed(self):
        """
        M1 counter speed and direction. Returned value is in pulses per
        second. RoboClaw keeps track of how many pulses received per
        second for both decoder channels.

        Uses:
        18 - Read Speed M1
        """
        raise NotImplementedError()

    @property
    def m2_counter_speed(self):
        """
        M2 counter speed and direction. Returned value is in pulses per
        second. RoboClaw keeps track of how many pulses received per
        second for both decoder channels.

        Uses:
        19 - Read Speed M2
        """
        raise NotImplementedError()
    
    def reset_encoders(self):
        """
        20 - Reset Quadrature Encoder Counters

        Will reset both quadrature decoder counters to zero.
        """
        raise NotImplementedError()

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
    def m1_velocity_pid(self, value):
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
        P = 0x00010000 
        I = 0x00008000 
        D = 0x00004000

        QPPS is the speed of the encoder when the motor is at 100% power.
        """
        raise NotImplementedError()

    @m2_velocity_pid.setter
    def m2_velocity_pid(self, value):
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
        P = 0x00010000
        I = 0x00008000
        D = 0x00004000
        
        QPPS is the speed of the encoder when the motor is at 100%
        power. P, I, D are the default values used after a reset.
        """
        raise NotImplementedError()
    
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
        raise NotImplementedError()

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
        raise NotImplementedError()

    def drive_m1_signed_duty(self, value):
        """
        32 - Drive M1 With Signed Duty Cycle

        Drive M1 using a duty cycle value. The duty cycle is used to
        control the speed of the motor without a quadrature
        encoder. The duty value is signed and the range is +/-1500.
        """
        raise NotImplementedError()

    def drive_m2_signed_duty(self, value):
        """
        33 - Drive M2 With Signed Duty Cycle

        Drive M2 using a duty cycle value. The duty cycle is used to
        control the speed of the motor without a quadrature
        encoder. The duty value is signed and the range is +/-1500.
        """
        raise NotImplementedError()

    def drive_mix_signed_duty(self, value_m1, value_m2):
        """
        34 - Mix Mode Drive M1 / M2 With Signed Duty Cycle

        Drive both M1 and M2 using a duty cycle value. The duty cycle
        is used to control the speed of the motor without a quadrature
        encoder. The duty value is signed and the range is +-1500.
        """
        raise NotImplementedError()

    def drive_m1_signed_speed(self, value):
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
        raise NotImplementedError()

    def drive_m2_signed_speed(self, value):
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
        raise NotImplementedError()

    def drive_mix_signed_speed(self, value_m1, value_m2):
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
        raise NotImplementedError()

    def drive_m1_signed_speed_acceleration(self, speed, acceleration):
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
        raise NotImplementedError()

    def drive_m2_signed_speed_acceleration(self, speed, acceleration):
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
        raise NotImplementedError()

    def drive_mix_signed_speed_acceleration(self, speed_m1, speed_m2, acceleration):
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
        raise NotImplementedError()

    def buffered_drive_m1_signed_speed_distance(self, speed, distance, buffered=True):
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
        raise NotImplementedError()

    def buffered_drive_m2_signed_speed_distance(self, speed, distance, buffered=True):
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
        raise NotImplementedError()

    def buffered_drive_mix_signed_speed_distance(self, speed_m1, distance_m1, speed_m2, distance_m2, buffered=True):
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
        raise NotImplementedError()

    def buffered_drive_m1_signed_speed_accel_distance(self, speed, acceleration, distance, buffered=True):
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
        raise NotImplementedError()

    def buffered_drive_m2_signed_speed_accel_distance(self, speed, acceleration, distance, buffered=True):
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
        raise NotImplementedError()

    def buffered_drive_mix_signed_speed_accel_distance(self, acceleration, speed_m1, distance_m1, speed_m2, distance_m2):
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
        raise NotImplementedError()

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
        raise NotImplementedError()

    def drive_mix_signed_speed_indiv_accels(self, acceleration_m1, speed_m1, acceleration_m2, speed_m2):
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
        raise NotImplementedError()

    def buffered_drive_mix_signed_speed_indiv_accel_distance(self, acceleration_m1, speed_m1, distance_m1, acceleration_m2, speed_m2, distance_m2, buffered=True):
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
        raise NotImplementedError()

    def drive_m1_signed_duty_accel(self, duty, acceleration):
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
        raise NotImplementedError()
    
    def drive_m2_signed_duty_accel(self, duty, acceleration):
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
        raise NotImplementedError()

    def drive_mix_signed_duty_accel(self, duty_m1, accel_m1, duty_m2, accel_m2):
        """
        Drive M1 and M2 in the same command using acceleration and
        duty values for each motor. The sign indicates which direction
        the motor will run. The acceleration value is not signed. This
        command is used to drive the motor by PWM using an
        acceleration value for ramping.
        
        The duty value is signed and the range is +/-1500.
        The accel value range is 0 to 65535.
        """
        raise NotImplementedError()

    @property 
    def m1_position_pid(self):
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
        raise NotImplementedError()

    @property 
    def m2_position_pid(self):
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
        raise NotImplementedError()

    def drive_m1_signed_speed_accel_decel_position(self, acceleration, speed, deceleration, position):
        """
        65 - Drive M1 with signed Speed, Accel, Deccel and Position

        Move M1 position from the current position to the specified
        new position and hold the new position. Accel sets the
        acceleration value and deccel the decceleration value. QSpeed
        sets the speed in quadrature pulses the motor will run at
        after acceleration and before decceleration.
        """
        raise NotImplementedError()

    def drive_m2_signed_speed_accel_decel_position(self, acceleration, speed, deceleration, position):
        """
        66 - Drive M2 with signed Speed, Accel, Deccel and Position

        Move M2 position from the current position to the specified
        new position and hold the new position. Accel sets the
        acceleration value and deccel the decceleration value. QSpeed
        sets the speed in quadrature pulses the motor will run at
        after acceleration and before decceleration.
        """
        raise NotImplementedError()

    def drive_mix_signed_speed_accel_decel_position(self, acceleration, speed, deceleration, position):
        """
        67 - Drive M1 & M2 with signed Speed, Accel, Deccel and Position

        Move M1 & M2 positions from their current positions to the
        specified new positions and hold the new positions. Accel sets
        the acceleration value and deccel the decceleration
        value. QSpeed sets the speed in quadrature pulses the motor
        will run at after acceleration and before decceleration.
        """
        # TODO: The parameters for this command in the docs seems wrong...
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
