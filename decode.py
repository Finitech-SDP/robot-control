import ev3dev.ev3 as ev3
import re
import config
import move

# from ev3dev2.motor import (
#     LargeMotor,
#     OUTPUT_A,
#     OUTPUT_B,
#     OUTPUT_C,
#     OUTPUT_D,
#     MoveTank,
#     MoveSteering,
# )


my_dict = {
    "F": move.moveForward,
    "B": move.moveBackward,
    "R": move.moveRight,
    "L": move.moveLeft,
    "FR": move.moveForwardLeft,
    "FL": move.moveForwardRight,
    "BR": move.moveBackwardRight,
    "BL": move.moveBackwardLeft,
    "RA": move.rotateAntiClockwise,
    "RC": move.rotateClockwise,
}


def decode(instruction_list):
    for m in instruction_list:
        move.FWDLEFT.wait_until_not_moving()
        move.BWDLEFT.wait_until_not_moving()
        move.FWDRIGHT.wait_until_not_moving()
        move.BWDRIGHT.wait_until_not_moving()
        if m.group(6) is None:  # Determine whether it is rotation command
            if m.group(3) is None:
                speed = config.D_SPEED  # by default 50% of its rated maximum speed
            else:
                speed = int(m.group(3))
            speed /= 100
            speed *= 1050
            if m.group(4) == "":
                time = config.D_SECONDS  # by default 1000ms
            else:
                time = int(m.group(4))
            direction = m.group(2)
            print(speed, time)
            my_dict[direction](speed, time)
        else:  # For rotate instruction
            direction = m.group(6)
            angle = int(m.group(7))
            my_dict[direction](angle)
