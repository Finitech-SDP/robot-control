import logging
import sys
from time import sleep, time

#import ev3dev.ev3 as ev3
#from ev3dev2.sensor.lego import GyroSensor
from motors import Motors
import config
from util import util

#FWDLEFT = ev3.LargeMotor("outA")  # outA means the motor connect to EV3 port A.
#FWDRIGHT = ev3.LargeMotor("outD")
#BWDLEFT = ev3.LargeMotor("outB")
#BWDRIGHT = ev3.LargeMotor("outC")
'''Motor_id represented'''
FWDLEFT = 0
FWDRIGHT = 1
BWDLEFT = 2
BWDRIGHT = 3
mc = Motors()

#GYRO = GyroSensor()
#GYRO.mode = "GYRO-ANG"

'''
def stop_when_rotation_complete(angle):
    c_angle = GYRO.angle
    iteration = 0
    last_angle = 0
    angle = int(angle)

    while abs(GYRO.angle - c_angle) < angle:
        if last_angle == GYRO.angle:
            iteration += 1
        else:
            iteration = 0

        last_angle = GYRO.angle
        if iteration == 50:
            break

        sleep(0.005)
        continue

    stop()
'''

"""@util.retry(on_fail_message="The motors aren't connected")
def is_motor_connected():
    return (
        FWDLEFT.connected
        and FWDRIGHT.connected
        and BWDLEFT.connected
        and BWDRIGHT.connected
    )"""

def stop_when_time_reach(time):
  curr_time = time()
  while time()<curr_time+time:
	    sleep(0.01)
  mc.stop_motors()

  
"""def exit_if_motors_not_connected():
    if not is_motor_connected():
        logging.critical("Motors are not properly connected, exiting...")
        sys.exit(1)"""


"""def wait_until_stationary():
    FWDLEFT.wait_until_not_moving(timeout=1250)
    BWDLEFT.wait_until_not_moving(timeout=1250)
    FWDRIGHT.wait_until_not_moving(timeout=1250)
    BWDRIGHT.wait_until_not_moving(timeout=1250)"""


def move_forward(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
 		if time == "-F":
        mc.move_motor(FWDRIGHT,speed)
        mc.move_motor(BWDLEFT,-speed) 
    else:
        time = int(time)
        mc.move_motor(FWDRIGHT,speed)
        mc.move_motor(BWDLEFT,-speed) 
        stop_when_time_reach(time)

def move_backward(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
    if time == "-F":
        mc.move_motor(FWDLEFT,speed)
        mc.move_motor(BWDRIGHT,+speed) 
    else:
        time = int(time)
				mc.move_motor(FWDLEFT,speed)
        mc.move_motor(BWDRIGHT,+speed) 
				stop_when_time_reach(time)

def move_left(speed, time):
		if time == "":
        time = config.DEFAULT_RUNTIME_MS
 		if time == "-F":
        mc.move_motor(FWDLEFT,speed)
        mc.move_motor(BWDRIGHT,-speed)  
    else:
        time = int(time)
        mc.move_motor(FWDLEFT,speed)
        mc.move_motor(BWDRIGHT,-speed) 
        stop_when_time_reach(time)

def move_right(speed, time):
		if time == "":
        time = config.DEFAULT_RUNTIME_MS
 		if time == "-F":
        mc.move_motor(FWDLEFT,-speed)
        mc.move_motor(BWDRIGHT,speed) 
    else:
        time = int(time)
        mc.move_motor(FWDLEFT,-speed)
        mc.move_motor(BWDRIGHT,speed) 
        stop_when_time_reach(time)

def move_forward_left(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
 		if time == "-F":
  
        mc.read_encoder()
    
    
        mc.move_motor(FWDRIGHT,speed)
        mc.move_motor(BWDLEFT,-speed) 
        mc.move_motor(FWDLEFT,speed)
        mc.move_motor(BWDRIGHT,-speed)
    else:
        time = int(time)
        mc.move_motor(FWDRIGHT,speed)
        mc.move_motor(BWDLEFT,-speed) 
        mc.move_motor(FWDLEFT,speed)
        mc.move_motor(BWDRIGHT,-speed) 
        stop_when_time_reach(time)


def move_forward_right(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
 		if time == "-F":
        mc.move_motor(FWDRIGHT,speed)
        mc.move_motor(BWDLEFT,-speed) 
        mc.move_motor(FWDLEFT,-speed)
        mc.move_motor(BWDRIGHT,speed)
    else:
        time = int(time)
        mc.move_motor(FWDRIGHT,speed)
        mc.move_motor(BWDLEFT,-speed) 
        mc.move_motor(FWDLEFT,-speed)
        mc.move_motor(BWDRIGHT,speed) 
        stop_when_time_reach(time)


def move_backward_left(speed, angle):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
 		if time == "-F":
        mc.move_motor(FWDRIGHT,-speed)
        mc.move_motor(BWDLEFT,speed) 
        mc.move_motor(FWDLEFT,speed)
        mc.move_motor(BWDRIGHT,-speed)
    else:
        time = int(time)
        mc.move_motor(FWDRIGHT,speed)
        mc.move_motor(BWDLEFT,-speed) 
        mc.move_motor(FWDLEFT,-speed)
        mc.move_motor(BWDRIGHT,speed) 
        stop_when_time_reach(time)


def move_backward_right(speed, angle):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
 		if time == "-F":
        mc.move_motor(FWDRIGHT,-speed)
        mc.move_motor(BWDLEFT,speed) 
        mc.move_motor(FWDLEFT,-speed)
        mc.move_motor(BWDRIGHT,speed)
    else:
        time = int(time)
        mc.move_motor(FWDRIGHT,speed)
        mc.move_motor(BWDLEFT,-speed) 
        mc.move_motor(FWDLEFT,speed)
        mc.move_motor(BWDRIGHT,+speed) 
        stop_when_time_reach(time)



def rotate_clockwise(speed):
   """" if angle == "":
        time = config.DEFAULT_RUNTIME_ANGLE
 		if angle == "-F":
        mc.move_motor(FWDRIGHT,-speed)
        mc.move_motor(BWDLEFT,-speed) 
        mc.move_motor(FWDLEFT,-speed)
        mc.move_motor(BWDRIGHT,-speed) 
    else:
        angle = int(angle)
        mc.move_motor(FWDRIGHT,-speed)
        mc.move_motor(BWDLEFT,-speed) 
        mc.move_motor(FWDLEFT,-speed)
        mc.move_motor(BWDRIGHT,-speed) 
        stop_when_time_reach(time) """
    
		while(mc.read_encoder(FWRIGHT)<1800):
        mc.move_motor(FWRIGHT,-speed)
        mc.move_motor(BWDLEFT,speed)  
   
        
def rotate_anti_clockwise(speed, angle):
    if angle == "":
        time = config.DEFAULT_RUNTIME_ANGLE
 		if angle == "-F":
        mc.move_motor(FWDRIGHT,-speed)
        mc.move_motor(BWDLEFT,-speed) 
        mc.move_motor(FWDLEFT,-speed)
        mc.move_motor(BWDRIGHT,-speed) 
    else:
        angle = int(angle)
        mc.move_motor(FWDRIGHT,-speed)
        mc.move_motor(BWDLEFT,-speed) 
        mc.move_motor(FWDLEFT,-speed)
        mc.move_motor(BWDRIGHT,-speed) 
        stop_when_time_reach(time)
