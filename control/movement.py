from time import sleep

import ev3dev.ev3 as ev3
from ev3dev2.sensor.lego import GyroSensor
import config


FWDLEFT = ev3.LargeMotor("outA")  # OutA means the motor connect to EV3 port A.
FWDRIGHT = ev3.LargeMotor("outD")
BWDLEFT = ev3.LargeMotor("outB")
BWDRIGHT = ev3.LargeMotor("outC")

GYRO = GyroSensor()
GYRO.mode = "GYRO-ANG"


def rotation_detect(angle):
    c_angle = GYRO.angle
    itreation = 0
    last_angle = 0
    angle = int(angle)
    while abs(GYRO.angle - c_angle) < angle:
        if last_angle == GYRO.angle:
            itreation += 1
        else:
            itreation = 0

        last_angle = GYRO.angle
        if itreation == 40:
            print("break")
            break
        sleep(0.005)
        continue
    stop()   


def wait_until_stationary():
    FWDLEFT.wait_until_not_moving(timeout=1250)
    BWDLEFT.wait_until_not_moving(timeout=1250)
    FWDRIGHT.wait_until_not_moving(timeout=1250)
    BWDRIGHT.wait_until_not_moving(timeout=1250)


def is_motor_connected():
    if (
        FWDLEFT.connected
        and FWDRIGHT.connected
        and BWDLEFT.connected
        and BWDRIGHT.connected
    ):
        return True

    return False


def move_forward(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
    if time == "-F":
        FWDLEFT.run_forever(speed_sp=speed)
        FWDRIGHT.run_forever(speed_sp=speed)
        BWDLEFT.run_forever(speed_sp=-speed)
        BWDRIGHT.run_forever(speed_sp=-speed)
    else:
        time = int(time)
        FWDRIGHT.run_timed(speed_sp=speed, time_sp=time)
        FWDLEFT.run_timed(speed_sp=speed, time_sp=time)
        BWDLEFT.run_timed(speed_sp=-speed, time_sp=time)
        BWDRIGHT.run_timed(speed_sp=-speed, time_sp=time)


def move_backward(speed, time):
    if time == "":
        time = config.DEFAULT_RUNTIME_MS
    if time == "-F":
        FWDLEFT.run_forever(speed_sp=-speed)
        FWDRIGHT.run_forever(speed_sp=-speed)
        BWDLEFT.run_forever(speed_sp=speed)
        BWDRIGHT.run_forever(speed_sp=speed)
    else:
        time = int(time)
        FWDRIGHT.run_timed(speed_sp=-speed, time_sp=time)
        FWDLEFT.run_timed(speed_sp=-speed, time_sp=time)
        BWDLEFT.run_timed(speed_sp=speed, time_sp=time)
        BWDRIGHT.run_timed(speed_sp=speed, time_sp=time)


def move_left():
    return None


def move_right():
    return None


def move_forward_left(speed, angle):
    if angle == "":
        angle = config.DEFAULT_ANGLE
    if angle == "-F":
        FWDLEFT.run_forever(speed_sp=speed)
        FWDRIGHT.run_forever(speed_sp=speed / 2)
        BWDLEFT.run_forever(speed_sp=-speed)
        BWDRIGHT.run_forever(speed_sp=-speed / 2)
    else:
        angle = int(angle)
        FWDLEFT.run_forever(speed_sp=speed)
        FWDRIGHT.run_forever(speed_sp=speed / 2)
        BWDLEFT.run_forever(speed_sp=-speed)
        BWDRIGHT.run_forever(speed_sp=-speed / 2)
        rotation_detect(angle)



def move_forward_right(speed, angle):
    if angle == "":
        angle = config.DEFAULT_ANGLE
    if angle == "-F":
        FWDLEFT.run_forever(speed_sp=speed / 2)
        FWDRIGHT.run_forever(speed_sp=speed)
        BWDLEFT.run_forever(speed_sp=-speed / 2)
        BWDRIGHT.run_forever(speed_sp=-speed)

    else:
        angle = int(angle)
        FWDLEFT.run_forever(speed_sp=speed / 2)
        FWDRIGHT.run_forever(speed_sp=speed)
        BWDLEFT.run_forever(speed_sp=-speed / 2)
        BWDRIGHT.run_forever(speed_sp=-speed)
        rotation_detect(angle)



def move_backward_left(speed, angle):
    if angle == "":
        angle = config.DEFAULT_ANGLE
    if angle == "-F":
        FWDLEFT.run_forever(speed_sp=-speed / 2)
        FWDRIGHT.run_forever(speed_sp=-speed)
        BWDLEFT.run_forever(speed_sp=speed / 2)
        BWDRIGHT.run_forever(speed_sp=speed)
    else:
        angle = int(angle)
        FWDLEFT.run_forever(speed_sp=-speed / 2)
        FWDRIGHT.run_forever(speed_sp=-speed)
        BWDLEFT.run_forever(speed_sp=speed / 2)
        BWDRIGHT.run_forever(speed_sp=speed)
        rotation_detect(angle)



def move_backward_right(speed, angle):
    if angle == "":
        angle = config.DEFAULT_ANGLE
    if angle == "-F":
        FWDLEFT.run_forever(speed_sp=-speed)
        FWDRIGHT.run_forever(speed_sp=-speed / 2)
        BWDLEFT.run_forever(speed_sp=speed)
        BWDRIGHT.run_forever(speed_sp=speed / 2)
    else:
        angle = int(angle)
        FWDLEFT.run_forever(speed_sp=-speed)
        FWDRIGHT.run_forever(speed_sp=-speed / 2)
        BWDLEFT.run_forever(speed_sp=speed)
        BWDRIGHT.run_forever(speed_sp=speed / 2)
        rotation_detect(angle)



def stop():
        FWDLEFT.stop(stop_action="brake")
        FWDRIGHT.stop(stop_action="brake")
        BWDLEFT.stop(stop_action="brake")
        BWDRIGHT.stop(stop_action="brake")


def rotate_clockwise(speed,angle):
    FWDLEFT.run_forever(speed_sp=speed)
    FWDRIGHT.run_forever(speed_sp=-speed)
    BWDLEFT.run_forever(speed_sp=-speed/2)
    BWDRIGHT.run_forever(speed_sp=speed/2)
    c_angle = GYRO.angle
    if angle != "-F":
        rotation_detect(angle)



def rotate_anti_clockwise(speed,angle):
    FWDLEFT.run_forever(speed_sp=-speed)
    FWDRIGHT.run_forever(speed_sp=speed)
    BWDLEFT.run_forever(speed_sp=speed/2)
    BWDRIGHT.run_forever(speed_sp=-speed/2)

    if angle != "-F":
        rotation_detect(angle)

