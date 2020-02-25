import logging
import sys
from time import sleep, time

#import ev3dev.ev3 as ev3
#from ev3dev2.sensor.lego import GyroSensor
from motors import Motors
import config
from util import util
import decoder

'''Motor_id represented'''
SH = 2
FH = 3
Left = 1
Right = 4 #postive speed means going backward
mc = Motors()
TIME = time()
time_pass = 0
iscatch = False

#GYRO = GyroSensor()
#GYRO.mode = "GYRO-ANG"


def setTime (t):
    global TIME
    TIME = float(t)


def stop_when_time_reach(t):
    decoder.time = t
    global time_pass
    setTime(t)
    curr_time = time()
    while time()<curr_time+TIME:
        sleep(0.01)
        time_pass = time() - curr_time
    mc.stop_motors()
    decoder.is_moving = False


  
"""def exit_if_motors_not_connected():
    if not is_motor_connected():
        logging.critical("Motors are not properly connected, exiting...")
        sys.exit(1)"""
def stop():
    mc.stop_motors()
    decoder.is_moving = False


"""def wait_until_stationary():
    FWDLEFT.wait_until_not_moving(timeout=1250)
    BWDLEFT.wait_until_not_moving(timeout=1250)
    FWDRIGHT.wait_until_not_moving(timeout=1250)
    BWDRIGHT.wait_until_not_moving(timeout=1250)"""


def move_backward(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_S
    if time == "-F":
        mc.move_motor(Left,speed)
        mc.move_motor(Right,-speed) 
    else:
        time = float(time)
        mc.move_motor(Left,speed)
        mc.move_motor(Right,-speed)
        stop_when_time_reach(time)

def move_forward(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_S
    if time == "-F":
        mc.move_motor(Left,-speed)
        mc.move_motor(Right,speed) 
    else:
        time = float(time)
        mc.move_motor(Left,-speed)
        mc.move_motor(Right,speed) 
        stop_when_time_reach(time)

def move_left(speed, time):
    if time == "":
        time = config.DEFAULT_SIDE_RUNTIME_S
    if time == "-F":
        mc.move_motor(SH,speed)
        mc.move_motor(FH,-speed)  
    else:
        time = float(time)
        mc.move_motor(SH,speed)
        mc.move_motor(FH,-speed)
        stop_when_time_reach(time)

def move_right(speed, time):
    if time == "":
        time = config.DEFAULT_SIDE_RUNTIME_S
    if time == "-F":
        mc.move_motor(SH,-speed)
        mc.move_motor(FH,speed) 
    else:
        time = float(time)
        mc.move_motor(SH,-speed)
        mc.move_motor(FH,speed) 
        stop_when_time_reach(time)

def move_backward_left(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_S
    if time == "-F":
        mc.move_motor(FH,-speed)
        mc.move_motor(SH,speed) 
        mc.move_motor(Left,speed)
        mc.move_motor(Right,-speed)
    else:
        time = float(time)
        mc.move_motor(FH,-speed)
        mc.move_motor(SH,speed) 
        mc.move_motor(Left,speed)
        mc.move_motor(Right,-speed)
        stop_when_time_reach(time)


def move_backward_right(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_S
    if time == "-F":
        mc.move_motor(Left,speed)
        mc.move_motor(Right,-speed) 
        mc.move_motor(SH,-speed)
        mc.move_motor(FH,speed)
    else:
        time = float(time)
        mc.move_motor(Left,speed)
        mc.move_motor(Right,-speed) 
        mc.move_motor(SH,-speed)
        mc.move_motor(FH,speed)
        stop_when_time_reach(time)


def move_forward_right(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_S
    if time == "-F":
        mc.move_motor(Left,-speed)
        mc.move_motor(Right,speed) 
        mc.move_motor(SH,speed)
        mc.move_motor(FH,-speed)
    else:
        time = float(time)
        mc.move_motor(Left,-speed)
        mc.move_motor(Right,speed) 
        mc.move_motor(SH,speed)
        mc.move_motor(FH,-speed)
        stop_when_time_reach(time)

def catch():
    global iscatch
    if not iscatch:
        mc.move_motor(5,-80)
        stop_when_time_reach(0.1)
        iscatch = True

def release():
    global iscatch
    if iscatch:
        mc.move_motor(5,80)
        stop_when_time_reach(0.1)
        iscatch = False

def move_forward_left(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_S
    if time == "-F":
        mc.move_motor(Left,-speed)
        mc.move_motor(Right,speed) 
        mc.move_motor(SH,-speed)
        mc.move_motor(FH,speed)
    else:
        time = float(time)
        mc.move_motor(Left,-speed)
        mc.move_motor(Right,speed) 
        mc.move_motor(SH,-speed)
        mc.move_motor(FH,speed)
        stop_when_time_reach(time)



def rotate_anti_clockwise(speed,angle):
    if angle == "-F":
        mc.move_motor(FH,speed)
        mc.move_motor(SH,speed)
        mc.move_motor(Left,speed)
        mc.move_motor(Right,speed)  
    else:
        mc.move_motor(FH,speed)
        mc.move_motor(SH,speed)
        mc.move_motor(Left,speed)
        mc.move_motor(Right,speed)   
        stop_when_time_reach(20)
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
   
        
def rotate_clockwise(speed, angle):
    # if angle == "":
    #     time = config.DEFAULT_RUNTIME_ANGLE
    # if angle == "-F":
    #     mc.move_motor(FWDRIGHT,-speed)
    #     mc.move_motor(BWDLEFT,-speed) 
    #     mc.move_motor(FWDLEFT,-speed)
    #     mc.move_motor(BWDRIGHT,-speed) 
    # else:
    #     angle = int(angle)
    #     mc.move_motor(FWDRIGHT,-speed)
    #     mc.move_motor(BWDLEFT,-speed) 
    #     mc.move_motor(FWDLEFT,-speed)
    #     mc.move_motor(BWDRIGHT,-speed) 
    #     stop_when_time_reach(time)
    if angle == '-F':
        mc.move_motor(FH,-speed)
        mc.move_motor(SH,-speed)  
        mc.move_motor(Left,-speed)
        mc.move_motor(Right,-speed)
    else :
        mc.move_motor(FH,-speed)
        mc.move_motor(SH,-speed)  
        mc.move_motor(Left,-speed)
        mc.move_motor(Right,-speed)
        stop_when_time_reach(20)