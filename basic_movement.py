import ev3dev.ev3 as ev3

# from ev3dev2.motor import (
#     LargeMotor,
#     OUTPUT_A,
#     OUTPUT_B,
#     OUTPUT_C,
#     OUTPUT_D,
#     MoveTank,
#     MoveSteering,
# )

FWDLEFT = ev3.LargeMotor("outA")  # OutA means the motor connect to EV3 port A.
FWDRIGHT = ev3.LargeMotor("outD")
BWDLEFT = ev3.LargeMotor("outB")
BWDRIGHT = ev3.LargeMotor("outC")


def isMotorConnected():
    if not (  # Check whether all the motor are connected.
        FWDLEFT.connected
        and FWDRIGHT.connected
        and BWDLEFT.connected
        and BWDRIGHT.connected
    ):
        return False
    return True


def moveFoward(speed, time):
    FWDRIGHT.run_timed(speed_sp=speed, time_sp=time)
    FWDLEFT.run_timed(speed_sp=speed, time_sp=time)
    BWDLEFT.run_timed(speed_sp=-speed, time_sp=time)
    BWDRIGHT.run_timed(speed_sp=-speed, time_sp=time)


def moveBackward(speed, time):
    FWDRIGHT.run_timed(speed_sp=-speed, time_sp=time)
    FWDLEFT.run_timed(speed_sp=-speed, time_sp=time)
    BWDLEFT.run_timed(speed_sp=speed, time_sp=time)
    BWDRIGHT.run_timed(speed_sp=speed, time_sp=time)


def moveLeft():
    return None


def moveRight():
    return None


def moveFowardLeft():
    return None


def moveFowardRight():
    return None


def moveBackwardLeft():
    return None


def moveBackwardRight():
    return None


def rotateAntiClockwise(angle):
    angle /= 360
    angle *= 1390
    FWDLEFT.run_to_rel_pos(position_sp=angle, speed_sp=300)
    FWDRIGHT.run_to_rel_pos(position_sp=-angle, speed_sp=300)
    BWDLEFT.run_to_rel_pos(position_sp=-angle, speed_sp=300)
    BWDRIGHT.run_to_rel_pos(position_sp=angle, speed_sp=300)


def rotateClockwise(angle):
    angle /= 360
    angle *= 1390
    FWDLEFT.run_to_rel_pos(position_sp=-angle, speed_sp=300)
    FWDRIGHT.run_to_rel_pos(position_sp=angle, speed_sp=300)
    BWDLEFT.run_to_rel_pos(position_sp=angle, speed_sp=300)
    BWDRIGHT.run_to_rel_pos(position_sp=-angle, speed_sp=300)