# sdp
# Introduction
This is the robot control script written in python.
Using scp main.py robot@ip_address:/home/robot to send the main script to the EV3 machine, run the script during the console.
And you can give simple commands to the EV3.
## Shortcut
# Direction
F: Forward
B: Backward
L: Left
R: Right
FR: FowardRight
FL: FowardLeft
BR: BackwardRight
BL: BackwardLeft
# Rotation
RA: Rotate anti clockwise
RC: Rotate clockwise
## Basic command format
### Direction speed time
Where speed has range 0-100, where 100 means it reaches EV3 motor's maximum rotate speed, 1050 degrees per second.
Time is in milliseconds.
### Rotation degree
Wherer degree should be within 360 degrees.
## To do
1. Store a list of command. Execute one by one.
2. Add a switch function between moving and stopping. i.e switch between run and idle.
(Add your thinking here!)