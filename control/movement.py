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
FRONT = 4
BACK = 1
SH = 2
FH = 3
mc = Motors()
TIME = time()
iscatch = False
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
def setTime (t):
    global TIME
    TIME = float(t)


def stop_when_time_reach(t):
    setTime(t)
    curr_time = time()
    while time()<curr_time+TIME:
        sleep(0.01)
    mc.stop_motors()


  
"""def exit_if_motors_not_connected():
    if not is_motor_connected():
        logging.critical("Motors are not properly connected, exiting...")
        sys.exit(1)"""
def stop():
    mc.stop_motors()

"""def wait_until_stationary():
    FWDLEFT.wait_until_not_moving(timeout=1250)
    BWDLEFT.wait_until_not_moving(timeout=1250)
    FWDRIGHT.wait_until_not_moving(timeout=1250)
    BWDRIGHT.wait_until_not_moving(timeout=1250)"""


def move_forward(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
    if time == "-F":
        mc.move_motor(FRONT,speed)
        mc.move_motor(BACK,-speed) 
    else:
        time = int(time)
        mc.move_motor(FRONT,speed)
        mc.move_motor(BACK,-speed)
        stop_when_time_reach(time)

def move_backward(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
    if time == "-F":
        mc.move_motor(FRONT,-speed)
        mc.move_motor(BACK,speed) 
    else:
        time = int(time)
        mc.move_motor(FRONT,-speed)
        mc.move_motor(BACK,speed) 
        stop_when_time_reach(time)

def move_left(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
    if time == "-F":
        mc.move_motor(SH,speed)
        mc.move_motor(FH,-speed)  
    else:
        time = int(time)
        mc.move_motor(SH,speed)
        mc.move_motor(FH,-speed)
        stop_when_time_reach(time)

def move_right(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
    if time == "-F":
        mc.move_motor(SH,-speed)
        mc.move_motor(FH,speed) 
    else:
        time = int(time)
        mc.move_motor(SH,-speed)
        mc.move_motor(FH,speed) 
        stop_when_time_reach(time)

def move_forward_left(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
    if time == "-F":
        mc.read_encoder()
        mc.move_motor(FH,-speed)
        mc.move_motor(SH,speed) 
        mc.move_motor(FRONT,speed)
        mc.move_motor(BACK,-speed)
    else:
        time = int(time)
        mc.move_motor(FH,-speed)
        mc.move_motor(SH,speed) 
        mc.move_motor(FRONT,speed)
        mc.move_motor(BACK,-speed)
        stop_when_time_reach(time)


def move_forward_right(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
    if time == "-F":
        mc.move_motor(FRONT,speed)
        mc.move_motor(BACK,-speed) 
        mc.move_motor(SH,-speed)
        mc.move_motor(FH,speed)
    else:
        time = int(time)
        mc.move_motor(FRONT,speed)
        mc.move_motor(BACK,-speed) 
        mc.move_motor(SH,-speed)
        mc.move_motor(FH,speed)
        stop_when_time_reach(time)


def move_backward_left(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
    if time == "-F":
        mc.move_motor(FRONT,-speed)
        mc.move_motor(BACK,speed) 
        mc.move_motor(SH,speed)
        mc.move_motor(FH,-speed)
    else:
        time = int(time)
        mc.move_motor(FRONT,-speed)
        mc.move_motor(BACK,speed) 
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

def move_backward_right(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
        if time == "-F":
            mc.move_motor(FRONT,-speed)
            mc.move_motor(BACK,speed) 
            mc.move_motor(SH,-speed)
            mc.move_motor(FH,speed)
    else:
        time = int(time)
        mc.move_motor(FRONT,-speed)
        mc.move_motor(BACK,speed) 
        mc.move_motor(SH,-speed)
        mc.move_motor(FH,speed)
        stop_when_time_reach(time)



def rotate_clockwise(speed,angle):
    mc.move_motor(FH,speed)
    mc.move_motor(SH,speed)  
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
   
        
def rotate_anti_clockwise(speed, angle):
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
    mc.move_motor(FH,-speed)
    mc.move_motor(SH,-speed)  
    stop_when_time_reach(20)