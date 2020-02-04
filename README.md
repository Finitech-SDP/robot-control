# SDP Robot Control

## Getting the code on EV3
At the moment we do not have a sophisticated way of getting code onto the EV3 - have to use scp:
```bash
scp -r robot-control robot@<ip-address>:/home/robot/robot-control
```
> \<ip-address> is usually 192.168.105.4

* Run `./main.py` on EV3 for an interactive command console
* Run `./main.py server` on EV3 for server remote control
### Interactive Console Commands
#### Direction identifiers
* F: Forward
* B: Backward
* L: Left
* R: Right
* FR: ForwardRight
* FL: ForwardLeft
* BR: BackwardRight
* BL: BackwardLeft
#### Rotation identifiers
* RA: Rotate anti clockwise
* RC: Rotate clockwise
#### Command format
`> [direction|rotation] [power] [time|angle]`

* power in range 0-100, where 100 means it reaches EV3 motor's maximum rotate speed, 1050 degrees per second.
* time is in milliseconds.
* rotation angle should be within 360 degrees.

