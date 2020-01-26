#! /usr/bin/env python3
import re
from ev3dev2.motor import (
    LargeMotor,
    OUTPUT_A,
    OUTPUT_B,
    OUTPUT_C,
    OUTPUT_D,
    MoveTank,
    MoveSteering,
)


def moveFoward(speed, time):
    fwdRight.on_for_seconds(speed, time)
    fwdLeft.on_for_seconds(speed, time)
    bwdLeft.on_for_seconds(-speed, time)
    bwdRight.on_for_seconds(-speed, time)


def moveBackward(speed, time):
    fwdRight.on_for_seconds(-speed, time)
    fwdLeft.on_for_seconds(-speed, time)
    bwdLeft.on_for_seconds(speed, time)
    bwdRight.on_for_seconds(speed, time)


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
    fwdLeft.on_for_rotations(speed=50, rotations=angle)
    fwdRight.on_for_rotations(speed=-50, rotations=angle)
    bwdLeft.on_for_rotations(speed=-50, rotations=angle)
    bwdRight.on_for_rotations(speed=50, rotations=angle)


def rotateAntiClockwise(angle):
    fwdLeft.on_for_rotations(speed=-50, rotations=angle)
    fwdRight.on_for_rotations(speed=50, rotations=angle)
    bwdLeft.on_for_rotations(speed=50, rotations=angle)
    bwdRight.on_for_rotations(speed=-50, rotations=angle)


# "((FR|FL|BL|BR|[FBRL]) (100|\d?\d)? (\d*))|((RA|RC) (360|3[0-5][0-9]|[0-2]?[0-9]{1,2}))"
command_re = "((FR|FL|BL|BR|[FBRL]) (100|\d?\d)? (\d*))|((RA|RC) (\d*))"
"""Our command's regular expression is
((FR|FL|BL|BR|[FBRL]) (100|\d?\d)? (\d*))|
    ((RA|RC) (360|3[0-5][0-9]|[0-2]?[0-9]{1,2}))
can be seen as [direction speed(percentage) duration(ms)] or
 [rotate_direction rotate angles]"""
fwdLeft = LargeMotor(OUTPUT_B)
fwdRight = LargeMotor(OUTPUT_A)
bwdLeft = LargeMotor(OUTPUT_D)
bwdRight = LargeMotor(OUTPUT_C)
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
