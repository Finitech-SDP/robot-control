import config
import re
from control import movement

DIRECTIONS = {
    "F": movement.move_forward,
    "B": movement.move_backward,
    "R": movement.move_right,
    "L": movement.move_left,
    "FR": movement.move_forward_left,
    "FL": movement.move_forward_right,
    "BR": movement.move_backward_right,
    "BL": movement.move_backward_left,
    "RA": movement.rotate_anti_clockwise,
    "RC": movement.rotate_clockwise,
}
INSTRUCTIONS = []
BEGIN_TRANSACTION = False


def parse_command(command):
    global BEGIN_TRANSACTION
    global INSTRUCTIONS

    command_pattern = "((FR|FL|BL|BR|[FBRL]) (100|\d?\d)? (-F|\d*))|((RA|RC) (-F|\d*))"
    if command == "STOP":
        movement.stop()
        return None
    if command == "BEGIN":
        BEGIN_TRANSACTION = True
        return None
    if command == "END":
        BEGIN_TRANSACTION = False
        decode(INSTRUCTIONS)
        INSTRUCTIONS.clear()
        return None
    match = re.fullmatch(command_pattern, command)

    if match is None:
        print("Incorrect command format")
    else:
        if BEGIN_TRANSACTION:
            INSTRUCTIONS.append(match)
        else:
            decode([match])


def decode(instructions):
    """ :param instructions is a list of command regex matches """

    for match in instructions:
        movement.wait_until_stationary()

        if match.group(6) is None:  # is it not a rotation command?
            if match.group(3) is None:
                speed = config.DEFAULT_SPEED_PERCENT
            else:
                speed = int(match.group(3))

            speed /= 100
            speed *= 1050

            time = match.group(4)

            direction = match.group(2)
            DIRECTIONS[direction](speed, time)
        else:
            direction = match.group(6)
            angle = match.group(7)
            DIRECTIONS[direction](angle)
