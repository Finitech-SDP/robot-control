from time import sleep

import ev3dev.ev3 as ev3
from ev3dev2.sensor.lego import GyroSensor

FWDLEFT = ev3.LargeMotor("outA")  # OutA means the motor connect to EV3 port A.
FWDRIGHT = ev3.LargeMotor("outD")
BWDLEFT = ev3.LargeMotor("outB")
BWDRIGHT = ev3.LargeMotor("outC")

GYRO = GyroSensor()
GYRO.mode = "GYRO-ANG"


def wait_until_stationary():
    FWDLEFT.wait_until_not_moving()
    BWDLEFT.wait_until_not_moving()
    FWDRIGHT.wait_until_not_moving()
    BWDRIGHT.wait_until_not_moving()


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
    FWDRIGHT.run_timed(speed_sp=speed, time_sp=time)
    FWDLEFT.run_timed(speed_sp=speed, time_sp=time)
    BWDLEFT.run_timed(speed_sp=-speed, time_sp=time)
    BWDRIGHT.run_timed(speed_sp=-speed, time_sp=time)


def move_backward(speed, time):
    FWDRIGHT.run_timed(speed_sp=-speed, time_sp=time)
    FWDLEFT.run_timed(speed_sp=-speed, time_sp=time)
    BWDLEFT.run_timed(speed_sp=speed, time_sp=time)
    BWDRIGHT.run_timed(speed_sp=speed, time_sp=time)


def move_left():
    return None


def move_right():
    return None


def move_forward_left(speed, time):
    FWDRIGHT.run_timed(speed_sp=speed / 2, time_sp=time)
    FWDLEFT.run_timed(speed_sp=speed, time_sp=time)
    BWDLEFT.run_timed(speed_sp=-speed, time_sp=time)
    BWDRIGHT.run_timed(speed_sp=-speed / 2, time_sp=time)


def move_forward_right(speed, time):
    FWDRIGHT.run_timed(speed_sp=speed, time_sp=time)
    FWDLEFT.run_timed(speed_sp=speed / 2, time_sp=time)
    BWDLEFT.run_timed(speed_sp=-speed / 2, time_sp=time)
    BWDRIGHT.run_timed(speed_sp=-speed, time_sp=time)


def move_backward_left(speed, time):
    FWDRIGHT.run_timed(speed_sp=-speed, time_sp=time)
    FWDLEFT.run_timed(speed_sp=-speed / 2, time_sp=time)
    BWDLEFT.run_timed(speed_sp=speed / 2, time_sp=time)
    BWDRIGHT.run_timed(speed_sp=speed, time_sp=time)


def move_backward_right(speed, time):
    FWDRIGHT.run_timed(speed_sp=-speed / 2, time_sp=time)
    FWDLEFT.run_timed(speed_sp=-speed, time_sp=time)
    BWDLEFT.run_timed(speed_sp=speed, time_sp=time)
    BWDRIGHT.run_timed(speed_sp=speed / 2, time_sp=time)


def stop():
    FWDLEFT.stop(stop_action="hold")
    FWDRIGHT.stop(stop_action="hold")
    BWDLEFT.stop(stop_action="hold")
    BWDRIGHT.stop(stop_action="hold")


def rotate_clockwise(angle):
    c_angle = GYRO.angle

    FWDLEFT.run_forever(speed_sp=200)
    FWDRIGHT.run_forever(speed_sp=-200)
    BWDLEFT.run_forever(speed_sp=-100)
    BWDRIGHT.run_forever(speed_sp=100)

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

    while abs(GYRO.angle - c_angle) < angle:
        sleep(0.01)
        continue

    stop()
