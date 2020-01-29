#! /usr/bin/env python3

import re
import decode

if __name__ == "__main__":
    # "((FR|FL|BL|BR|[FBRL]) (100|\d?\d)? (\d*))|((RA|RC) (360|3[0-5][0-9]|[0-2]?[0-9]{1,2}))"
    """Our command's format is
    [direction speed(percentage of maximum rotate speed) duration(in ms)] or
    [rotate_direction rotate angles]"""
    command_re = "((FR|FL|BL|BR|[FBRL]) (100|\d?\d)? (\d*))|((RA|RC) (\d*))"
    begin_list = False
    instuction_set = []

    while True:
        if not decode.isMotorConnected():
            print("Motor is not well connected.")
            break
        command = input(">")  # Fetch input command.
        if command == "BEGIN":
            begin_list = True
            continue
        if command == "END":
            begin_list = False
            decode.decode(instuction_set)
            instuction_set.clear()
            continue
        m = re.fullmatch(command_re, command)
        if m is None:
            print("Command is not in correct format!")
        else:
            if begin_list:
                instuction_set.append(m)
            else:
                decode.decode([m])
