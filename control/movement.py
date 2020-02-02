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


def move_forward_left(speed, degree):
    if degree == "":
        degree = config.DEFAULT_RUNTIME_DEGREE
    if degree == "-F":
        FWDLEFT.run_forever(speed_sp=speed)
        FWDRIGHT.run_forever(speed_sp=speed / 2)
        BWDLEFT.run_forever(speed_sp=-speed)
        BWDRIGHT.run_forever(speed_sp=-speed / 2)
    else:
        degree = int(degree)
        c_degree = GYRO.angle
        FWDLEFT.run_forever(speed_sp=speed)
        FWDRIGHT.run_forever(speed_sp=speed / 2)
        BWDLEFT.run_forever(speed_sp=-speed)
        BWDRIGHT.run_forever(speed_sp=-speed / 2)
        while abs(GYRO.angle - c_degree) < degree:
            sleep(0.01)
            continue

        stop()


def move_forward_right(speed, degree):
    if degree == "":
        degree = config.DEFAULT_RUNTIME_DEGREE
    if degree == "-F":
        FWDLEFT.run_forever(speed_sp=speed / 2)
        FWDRIGHT.run_forever(speed_sp=speed)
        BWDLEFT.run_forever(speed_sp=-speed / 2)
        BWDRIGHT.run_forever(speed_sp=-speed)

    else:
        degree = int(degree)
        c_degree = GYRO.angle
        FWDLEFT.run_forever(speed_sp=speed / 2)
        FWDRIGHT.run_forever(speed_sp=speed)
        BWDLEFT.run_forever(speed_sp=-speed / 2)
        BWDRIGHT.run_forever(speed_sp=-speed)
        while abs(GYRO.angle - c_degree) < degree:
            sleep(0.01)
            continue

        stop()


def move_backward_left(speed, degree):
    if degree == "":
        degree = config.DEFAULT_RUNTIME_DEGREE
    if degree == "-F":
        FWDLEFT.run_forever(speed_sp=-speed / 2)
        FWDRIGHT.run_forever(speed_sp=-speed)
        BWDLEFT.run_forever(speed_sp=speed / 2)
        BWDRIGHT.run_forever(speed_sp=speed)
    else:
        degree = int(degree)
        c_degree = GYRO.angle
        FWDLEFT.run_forever(speed_sp=-speed / 2)
        FWDRIGHT.run_forever(speed_sp=-speed)
        BWDLEFT.run_forever(speed_sp=speed / 2)
        BWDRIGHT.run_forever(speed_sp=speed)
        while abs(GYRO.angle - c_degree) < degree:
            sleep(0.01)
            continue

        stop()


def move_backward_right(speed, degree):
    if degree == "":
        degree = config.DEFAULT_RUNTIME_DEGREE
    if degree == "-F":
        FWDLEFT.run_forever(speed_sp=-speed)
        FWDRIGHT.run_forever(speed_sp=-speed / 2)
        BWDLEFT.run_forever(speed_sp=speed)
        BWDRIGHT.run_forever(speed_sp=speed / 2)
    else:
        degree = int(degree)
        c_degree = GYRO.angle
        FWDLEFT.run_forever(speed_sp=-speed)
        FWDRIGHT.run_forever(speed_sp=-speed / 2)
        BWDLEFT.run_forever(speed_sp=speed)
        BWDRIGHT.run_forever(speed_sp=speed / 2)
        while abs(GYRO.angle - c_degree) < degree:
            sleep(0.01)
            continue

        stop()


def stop():
    FWDLEFT.stop(stop_action="brake")
    FWDRIGHT.stop(stop_action="brake")
    BWDLEFT.stop(stop_action="brake")
    BWDRIGHT.stop(stop_action="brake")


def rotate_clockwise(angle):
    c_angle = GYRO.angle

    FWDLEFT.run_forever(speed_sp=200)
    FWDRIGHT.run_forever(speed_sp=-200)
    BWDLEFT.run_forever(speed_sp=-100)
    BWDRIGHT.run_forever(speed_sp=100)

    if angle != "-F":
        angle = int(angle)
        while abs(GYRO.angle - c_angle) < angle:
            sleep(0.01)
            continue

        stop()


def rotate_anti_clockwise(angle):
    c_angle = GYRO.angle

    FWDLEFT.run_forever(speed_sp=-200)
    FWDRIGHT.run_forever(speed_sp=200)
    BWDLEFT.run_forever(speed_sp=100)
    BWDRIGHT.run_forever(speed_sp=-100)

    if angle != "-F":
        angle = int(angle)
        while abs(GYRO.angle - c_angle) < angle:
            sleep(0.01)
            continue

        stop()
