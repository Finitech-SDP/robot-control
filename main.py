#! /usr/bin/env python3
import re

from control import decoder
from control import movement


def main():
    command_pattern = "((FR|FL|BL|BR|[FBRL]) (100|\d?\d)? (\d*))|((RA|RC) (\d*))"
    begin_transaction = False
    instructions = []

    while True:
        if not movement.is_motor_connected():
            print("Motor is not connected properly")
            break

        command = input(">")

        if command == "STOP":
            movement.stop()
            continue
        if command == "BEGIN":
            begin_transaction = True
            continue
        if command == "END":
            begin_transaction = False
            decoder.decode(instructions)
            instructions.clear()
            continue

        match = re.fullmatch(command_pattern, command)

        if match is None:
            print("Incorrect command format")
        else:
            if begin_transaction:
                instructions.append(match)
            else:
                decoder.decode([match])


if __name__ == "__main__":
    main()
