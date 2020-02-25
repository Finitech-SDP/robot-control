import re

import config
from control import movement

direction = ""
speed = config.DEFAULT_SPEED_PERCENT
time = ""
is_moving = False

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

command_pattern = "(FR|FL|BL|BR|RA|RC|[FBRL]) (\d?\d?\d)? (-F|\d*.?\d*)?"
prog = re.compile(command_pattern)


    
def parse_command(command):

    if command == "STOP":
        movement.stop()
        return
    if command == "catch":
        movement.catch()
        return
    if command == "release":
        movement.release()
        return
    match = prog.match(command)

    if match is None:
        print("Incorrect command format")
    else:
        decode(match)

# def redo():
#     global time
#     global is_moving
#     if direction != "":
#         if time=="-F" :
#             is_moving = True
#             DIRECTIONS[direction](speed,'-F')
#         elif time == "":
#             pass
#         else :
#             is_moving = True
#             time = float(time) - movement.time_pass
#             print("%d seconds"%time)
#             DIRECTIONS[direction](speed,time)
        

def decode(match):
    global direction
    global speed
    global time
    global is_moving
    #movement.wait_until_stationary()

    if match.group(2) is None:
        speed = config.DEFAULT_SPEED_PERCENT
    else:
        speed = int(match.group(2))
    
    time = match.group(3)
    print (time)
    direction = match.group(1)
    is_moving =True
    DIRECTIONS[direction](speed, time)
    
