#! /usr/bin/env python3
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
import ev3dev.ev3 as ev3


def moveFoward(speed, time):
    fwdRight.run_timed(speed_sp=speed, time_sp=time)
    fwdLeft.run_timed(speed_sp=speed, time_sp=time)
    bwdLeft.run_timed(speed_sp=-speed, time_sp=time)
    bwdRight.run_timed(speed_sp=-speed, time_sp=time)


def moveBackward(speed, time):
    fwdRight.run_timed(speed_sp=-speed, time_sp=time)
    fwdLeft.run_timed(speed_sp=-speed, time_sp=time)
    bwdLeft.run_timed(speed_sp=speed, time_sp=time)
    bwdRight.run_timed(speed_sp=speed, time_sp=time)


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


def rotateClockwise(angle):
    angle /= 360
    angle *= 1390
    fwdLeft.run_to_rel_pos(position_sp=angle, speed_sp=300)
    fwdRight.run_to_rel_pos(position_sp=-angle, speed_sp=300)
    bwdLeft.run_to_rel_pos(position_sp=-angle, speed_sp=300)
    bwdRight.run_to_rel_pos(position_sp=angle, speed_sp=300)


def rotateAntiClockwise(angle):
    angle /= 360
    angle *= 1390
    fwdLeft.run_to_rel_pos(position_sp=-angle, speed_sp=300)
    fwdRight.run_to_rel_pos(position_sp=angle, speed_sp=300)
    bwdLeft.run_to_rel_pos(position_sp=angle, speed_sp=300)
    bwdRight.run_to_rel_pos(position_sp=-angle, speed_sp=300)


# "((FR|FL|BL|BR|[FBRL]) (100|\d?\d)? (\d*))|((RA|RC) (360|3[0-5][0-9]|[0-2]?[0-9]{1,2}))"
command_re = "((FR|FL|BL|BR|[FBRL]) (100|\d?\d)? (\d*))|((RA|RC) (\d*))"
"""Our command's regular expression is
((FR|FL|BL|BR|[FBRL]) (100|\d?\d)? (\d*))|
    ((RA|RC) (360|3[0-5][0-9]|[0-2]?[0-9]{1,2}))
can be seen as [direction speed(percentage) duration(ms)] or
 [rotate_direction rotate angles]"""
# fwdLeft = LargeMotor(OUTPUT_B)
# fwdRight = LargeMotor(OUTPUT_A)
# bwdLeft = LargeMotor(OUTPUT_D)
# bwdRight = LargeMotor(OUTPUT_C)
fwdLeft = ev3.LargeMotor("outB")
fwdRight = ev3.LargeMotor("outA")
bwdLeft = ev3.LargeMotor("outD")
bwdRight = ev3.LargeMotor("outC")
if not (
    fwdLeft.connected
    and fwdRight.connected
    and bwdLeft.connected
    and bwdRight.connected
):
    print("motor are not connected")
while True:
    command = input(">")
    m = re.fullmatch(command_re, command)
    if m is None:
        print("Command is not in correct format!")
    else:
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
