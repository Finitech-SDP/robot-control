#! /usr/bin/env python3

import re
import basic_movement as move


def decode(instruction_list):
    for m in instruction_list:
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
                move.moveFoward(speed, time)
            if direction == "B":
                move.oveBackward(speed, time)
            if direction == "R":
                move.moveRight()
            if direction == "L":
                move.moveLeft()
            if direction == "FR":
                move.moveFowardRight()
            if direction == "FL":
                move.moveFowardLeft()
            if direction == "BR":
                move.moveBackwardRight
            if direction == "BL":
                move.moveBackwardLeft()
        else:  # For rotate instruction
            direction = m.group(6)
            angle = int(m.group(7))
            if direction == "RA":
                move.rotateClockwise(angle)
            else:
                move.rotateAntiClockwise(angle)


if __name__ == "__main__":
    # "((FR|FL|BL|BR|[FBRL]) (100|\d?\d)? (\d*))|((RA|RC) (360|3[0-5][0-9]|[0-2]?[0-9]{1,2}))"
    """Our command's format is
    [direction speed(percentage of maximum rotate speed) duration(in ms)] or
    [rotate_direction rotate angles]"""
    command_re = "((FR|FL|BL|BR|[FBRL]) (100|\d?\d)? (\d*))|((RA|RC) (\d*))"
    begin_list = False
    instuction_set = []

    while True:
        if not move.isMotorConnected():
            print("Motor is not well connected.")
            break
        command = input(">")  # Fetch input command.
        if input == "BEGIN":
            begin_list = True
        if input == "END":
            begin_list = False
            decode(instuction_set)
            instuction_set.clear()
        m = re.fullmatch(command_re, command)
        if m is None:
            print("Command is not in correct format!")
        else:
            if begin_list:
                instuction_set.append(m)
            else:
                decode([m])
