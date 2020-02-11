import re

import config
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

def fullmatch(regex, string, flags=0):
    """Emulate python-3.4 re.fullmatch()."""
    return re.match("(?:" + regex + r")\Z", string, flags=flags)

def parse_command(command):
    command_pattern = "((FR|FL|BL|BR|RA|RC|[FBRL]) (100|\d?\d)? (-F|\d*))"

    if command == "STOP":
        movement.stop()
        return

    match = fullmatch(command_pattern, command)

    if match is None:
        print("Incorrect command format")
    else:
        decode(match)


def decode(match):
    #movement.wait_until_stationary()

    if match.group(3) is None:
        speed = config.DEFAULT_SPEED_PERCENT
    else:
        speed = int(match.group(3))

    speed /= 100
    speed *= 1050

    time = match.group(4)

    direction = match.group(2)
    DIRECTIONS[direction](speed, time)
