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
