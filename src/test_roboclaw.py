import roboclaw
from roboclaw import *
import serial

print "Roboclaw Example 1\r\n"

#Rasberry Pi/Linux Serial instance example
#port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=0.1)

#Windows Serial instance example
port = serial.Serial("/dev/ttyACM1", baudrate=38400, timeout=1)
roboclaw.port = port

#Get version string
sendcommand(128,21);
rcv = port.read(32)
print repr(rcv)

cnt = 0
while True:
	cnt=cnt+1
	print "Count = ",cnt
	
	print "Error State:",repr(readerrorstate())

	print "Temperature:",readtemperature()/10.0

	print "Main Battery:",readmainbattery()/10.0
	
	print "Logic Battery:",readlogicbattery()/10.0

	print "M1 Encoder:", readM1encoder()
	print "M2 Encoder:", readM2encoder()

	m1cur, m2cur = readcurrents();
	print "Current M1: ",m1cur/10.0," M2: ",m2cur/10.0
	
	min, max = readlogicbatterysettings()
	print "Logic Battery Min:",min/10.0," Max:",max/10.0

	min, max = readmainbatterysettings()
	print "Main Battery Min:",min/10.0," Max:",max/10.0

	p,i,d,qpps = readM1pidq()
	print "M1 P=%.2f" % (p/65536.0)
	print "M1 I=%.2f" % (i/65536.0)
	print "M1 D=%.2f" % (d/65536.0)
	print "M1 QPPS=",qpps

	p,i,d,qpps = readM2pidq()
	print "M2 P=%.2f" % (p/65536.0)
	print "M2 I=%.2f" % (i/65536.0)
	print "M2 D=%.2f" % (d/65536.0)
	print "M2 QPPS=",qpps

#	SetM1DutyAccel(1500,1500)
#	SetM2DutyAccel(1500,-1500)
#	time.sleep(2)
#	SetM1DutyAccel(1500,-1500)
#	SetM2DutyAccel(1500,1500)
#	time.sleep(2)
	time.sleep(0.5)

