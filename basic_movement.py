import ev3dev.ev3 as ev3
import re

# from ev3dev2.motor import (
#     LargeMotor,
#     OUTPUT_A,
#     OUTPUT_B,
#     OUTPUT_C,
#     OUTPUT_D,
#     MoveTank,
#     MoveSteering,
# )

FWDLEFT = ev3.LargeMotor("outA")  # OutA means the motor connect to EV3 port A.
FWDRIGHT = ev3.LargeMotor("outD")
BWDLEFT = ev3.LargeMotor("outB")
BWDRIGHT = ev3.LargeMotor("outC")


def isMotorConnected():
    if not (  # Check whether all the motor are connected.
        FWDLEFT.connected
        and FWDRIGHT.connected
        and BWDLEFT.connected
        and BWDRIGHT.connected
    ):
        return False
    return True


def moveFoward(speed, time):
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


def moveFowardLeft():
    return None


def moveFowardRight():
    return None


def moveBackwardLeft():
    return None


def moveBackwardRight():
    return None


def rotateAntiClockwise(angle):
    angle /= 360
    angle *= 1622
    FWDLEFT.run_to_rel_pos(position_sp=angle, speed_sp=200)
    FWDRIGHT.run_to_rel_pos(position_sp=-angle, speed_sp=200)
    BWDLEFT.run_to_rel_pos(position_sp=-angle, speed_sp=200)
    BWDRIGHT.run_to_rel_pos(position_sp=angle, speed_sp=200)


def rotateClockwise(angle):
    angle /= 360
    angle *= 1622
    FWDLEFT.run_to_rel_pos(position_sp=-angle, speed_sp=200)
    FWDRIGHT.run_to_rel_pos(position_sp=angle, speed_sp=200)
    BWDLEFT.run_to_rel_pos(position_sp=angle, speed_sp=200)
    BWDRIGHT.run_to_rel_pos(position_sp=-angle, speed_sp=200)


def decode(instruction_list):
    for m in instruction_list:
        FWDLEFT.wait_until_not_moving()
        BWDLEFT.wait_until_not_moving()
        FWDRIGHT.wait_until_not_moving()
        BWDRIGHT.wait_until_not_moving()
        if m.group(6) is None:  # Determine whether it is rotation command
            if m.group(3) is None:
                speed = 50  # by default 50% of its rated maximum speed
            else:
                speed = int(m.group(3))
            speed /= 100
            speed *= 1050
            if m.group(4) == "":
                time = 1000  # by default 1000ms
            else:
                time = int(m.group(4))
            direction = m.group(2)
            if direction == "F":
                moveFoward(speed, time)
            if direction == "B":
                moveBackward(speed, time)
            if direction == "R":
                moveRight()
            if direction == "L":
                moveLeft()
            if direction == "FR":
                moveFowardRight()
            if direction == "FL":
                moveFowardLeft()
            if direction == "BR":
                moveBackwardRight
            if direction == "BL":
                moveBackwardLeft()
        else:  # For rotate instruction
            direction = m.group(6)
            angle = int(m.group(7))
            if direction == "RA":
                rotateClockwise(angle)
            else:
                rotateAntiClockwise(angle)
