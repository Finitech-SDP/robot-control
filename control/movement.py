import logging
import sys
from time import sleep

import ev3dev.ev3 as ev3
from ev3dev2.sensor.lego import GyroSensor

import config
from util import util

FWDLEFT = ev3.LargeMotor("outA")  # outA means the motor connect to EV3 port A.
FWDRIGHT = ev3.LargeMotor("outD")
BWDLEFT = ev3.LargeMotor("outB")
BWDRIGHT = ev3.LargeMotor("outC")

GYRO = GyroSensor()
GYRO.mode = "GYRO-ANG"


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


@util.retry(on_fail_message="The motors aren't connected")
def is_motor_connected():
    return (
        FWDLEFT.connected
        and FWDRIGHT.connected
        and BWDLEFT.connected
        and BWDRIGHT.connected
    )


def exit_if_motors_not_connected():
    if not is_motor_connected():
        logging.critical("Motors are not properly connected, exiting...")
        sys.exit(1)


def wait_until_stationary():
    FWDLEFT.wait_until_not_moving(timeout=1250)
    BWDLEFT.wait_until_not_moving(timeout=1250)
    FWDRIGHT.wait_until_not_moving(timeout=1250)
    BWDRIGHT.wait_until_not_moving(timeout=1250)


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

        stop_when_rotation_complete(angle)


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

        stop_when_rotation_complete(angle)


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

        stop_when_rotation_complete(angle)


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

        stop_when_rotation_complete(angle)


def stop():
    FWDLEFT.stop(stop_action="brake")
    FWDRIGHT.stop(stop_action="brake")
    BWDLEFT.stop(stop_action="brake")
    BWDRIGHT.stop(stop_action="brake")


def rotate_clockwise(speed, angle):
    FWDLEFT.run_forever(speed_sp=speed)
    FWDRIGHT.run_forever(speed_sp=-speed)
    BWDLEFT.run_forever(speed_sp=-speed)
    BWDRIGHT.run_forever(speed_sp=speed)

    if angle != "-F":
        stop_when_rotation_complete(angle)


def rotate_anti_clockwise(speed, angle):
    FWDLEFT.run_forever(speed_sp=-speed)
    FWDRIGHT.run_forever(speed_sp=speed)
    BWDLEFT.run_forever(speed_sp=speed)
    BWDRIGHT.run_forever(speed_sp=-speed)

    if angle != "-F":
        stop_when_rotation_complete(angle)
