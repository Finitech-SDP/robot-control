import ev3dev.ev3 as ev3
import config
from ev3dev2.sensor.lego import GyroSensor
import math
from time import sleep


FWDLEFT = ev3.LargeMotor("outA")  # OutA means the motor connect to EV3 port A.
FWDRIGHT = ev3.LargeMotor("outD")
BWDLEFT = ev3.LargeMotor("outB")
BWDRIGHT = ev3.LargeMotor("outC")
gy = GyroSensor()
gy.mode = "GYRO-ANG"


def isMotorConnected():
    if not (  # Check whether all the motor are connected.
        FWDLEFT.connected
        and FWDRIGHT.connected
        and BWDLEFT.connected
        and BWDRIGHT.connected
    ):
        return False
    return True


def moveForward(speed, time):
    FWDRIGHT.run_timed(speed_sp=speed, time_sp=time)
    FWDLEFT.run_timed(speed_sp=speed, time_sp=time)
    BWDLEFT.run_timed(speed_sp=-speed, time_sp=time)
    BWDRIGHT.run_timed(speed_sp=-speed, time_sp=time)


def moveBackward(speed, time):
    FWDRIGHT.run_timed(speed_sp=-speed, time_sp=time)
    FWDLEFT.run_timed(speed_sp=-speed, time_sp=time)
    BWDLEFT.run_timed(speed_sp=speed, time_sp=time)
    BWDRIGHT.run_timed(speed_sp=speed, time_sp=time)


def moveLeft():
    return None


def moveRight():
    return None


def moveForwardLeft():
    return None


def moveForwardRight():
    return None


def moveBackwardLeft():
    return None


def moveBackwardRight():
    return None


def stop():
    FWDLEFT.stop(stop_action="hold")
    FWDRIGHT.stop(stop_action="hold")
    BWDLEFT.stop(stop_action="hold")
    BWDRIGHT.stop(stop_action="hold")


def rotateClockwise(angles):
    c_angle = gy.angle
    FWDLEFT.run_forever(speed_sp=200)
    FWDRIGHT.run_forever(speed_sp=-200)
    BWDLEFT.run_forever(speed_sp=-100)
    BWDRIGHT.run_forever(speed_sp=100)
    while abs(gy.angle - c_angle) < angles:
        continue
    stop()


def rotateAntiClockwise(angles):
    c_angle = gy.angle
    FWDLEFT.run_forever(speed_sp=-200)
    FWDRIGHT.run_forever(speed_sp=200)
    BWDLEFT.run_forever(speed_sp=100)
    BWDRIGHT.run_forever(speed_sp=-100)
    while abs(gy.angle - c_angle) < angles:
        sleep(0.01)
        continue
    stop()
