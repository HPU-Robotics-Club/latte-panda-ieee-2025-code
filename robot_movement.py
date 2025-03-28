from pyfirmata import Arduino, util

import robot

#These are the pins, meaning front/rear driver/passenger
FD_ENA = 0
FD_1 = 0
FD_2 = 1
FP_ENA = 2
FP_1 = 7
FP_2 = 8
RD_ENB = 1
RD_1 = 2
RD_2 = 3
RP_ENB = 3
RP_1 = 9
RP_2 = 10
ARM_SERVO = 12

#These are all of the direction constants
D_FORWARD        = 0
D_BACKWARD       = 1
D_LEFT           = 2
D_RIGHT          = 3
D_FORWARD_LEFT   = 4
D_FORWARD_RIGHT  = 5
D_BACKWARD_LEFT  = 6
D_BACKWARD_RIGHT = 7
D_END            = 8 #Stops the robot's motion

#These are here for some reason to make it easy to change the code later maybe
MOTOR_FORWARD    =  1
MOTOR_BACKWARD   = -1
MOTOR_OFF        =  0

#These are the rotation constant
R_CW             = 0
R_CCW            = 1
R_END            = 2 #Stops the robot's motion


def stop_motion():
    drive_motor(FD_1, FD_2, 0)
    drive_motor(RD_1, RD_2, 0)
    drive_motor(FP_1, FP_2, 0)
    drive_motor(RP_1, RP_2, 0)

#Start move8 Defintion
def move8(direction):
    speed = 255
    robot.board.analog[FD_ENA].write(speed)
    robot.board.analog[FP_ENA].write(speed)
    robot.board.analog[RD_ENB].write(speed)
    robot.board.analog[RP_ENB].write(speed)

    if direction == D_FORWARD: #Forward
        drive_motor(FD_1, FD_2, MOTOR_FORWARD)
        drive_motor(FP_1, FP_2, MOTOR_FORWARD)
        drive_motor(RD_1, RD_2, MOTOR_FORWARD)
        drive_motor(RP_1, RP_2, MOTOR_FORWARD)

    elif direction == D_BACKWARD:#Backward
        drive_motor(FD_1, FD_2, MOTOR_BACKWARD)
        drive_motor(FP_1, FP_2, MOTOR_BACKWARD)
        drive_motor(RD_1, RD_2, MOTOR_BACKWARD)
        drive_motor(RP_1, RP_2, MOTOR_BACKWARD)

    elif direction == D_LEFT:#Left
        drive_motor(FD_1, FD_2, MOTOR_FORWARD)
        drive_motor(FP_1, FP_2, MOTOR_BACKWARD)
        drive_motor(RD_1, RD_2, MOTOR_BACKWARD)
        drive_motor(RP_1, RP_2, MOTOR_FORWARD)

    elif direction == D_RIGHT:#Right
        drive_motor(FD_1, FD_2, MOTOR_BACKWARD)
        drive_motor(FP_1, FP_2, MOTOR_FORWARD)
        drive_motor(RD_1, RD_2, MOTOR_FORWARD)
        drive_motor(RP_1, RP_2, MOTOR_BACKWARD)

    elif direction == D_FORWARD_RIGHT:#Forward Right
        drive_motor(FD_1, FD_2, MOTOR_FORWARD)
        drive_motor(FP_1, FP_2, MOTOR_OFF)
        drive_motor(RD_1, RD_2, MOTOR_OFF)
        drive_motor(RP_1, RP_2, MOTOR_FORWARD)

    elif direction == D_FORWARD_LEFT:#Forward Left
        drive_motor(FD_1, FD_2, MOTOR_OFF)
        drive_motor(FP_1, FP_2, MOTOR_FORWARD)
        drive_motor(RD_1, RD_2, MOTOR_FORWARD)
        drive_motor(RP_1, RP_2, MOTOR_OFF)

    #NOTE I am not sure these two are correct
    elif direction == D_BACKWARD_LEFT:#Backward Left
        drive_motor(FD_1, FD_2, MOTOR_BACKWARD)
        drive_motor(FP_1, FP_2, MOTOR_OFF)
        drive_motor(RD_1, RD_2, MOTOR_OFF)
        drive_motor(RP_1, RP_2, MOTOR_BACKWARD)

    elif direction == D_BACKWARD_RIGHT: #Backward Right
        drive_motor(FD_1, FD_2, MOTOR_OFF)
        drive_motor(FP_1, FP_2, MOTOR_BACKWARD)
        drive_motor(RD_1, RD_2, MOTOR_BACKWARD)
        drive_motor(RP_1, RP_2, MOTOR_OFF)

    elif direction == D_END: #Ends Movement
        drive_motor(FD_1, FD_2, MOTOR_OFF)
        drive_motor(RD_1, RD_2, MOTOR_OFF)
        drive_motor(FP_1, FP_2, MOTOR_OFF)
        drive_motor(RP_1, RP_2, MOTOR_OFF)
#End move8 Defintion

#Start rotate Definition
def rotate(direction):
    if direction == R_CW:
        drive_motor(FD_1, FD_2, MOTOR_FORWARD)
        drive_motor(RD_1, RD_2, MOTOR_FORWARD)
        drive_motor(FP_1, FP_2, MOTOR_BACKWARD)
        drive_motor(RP_1, RP_2, MOTOR_BACKWARD)
    elif direction ==  R_CCW:
        drive_motor(FD_1, FD_2, MOTOR_BACKWARD)
        drive_motor(RD_1, RD_2, MOTOR_BACKWARD)
        drive_motor(FP_1, FP_2, MOTOR_FORWARD)
        drive_motor(RP_1, RP_2, MOTOR_FORWARD)
    elif direction == R_END:
        drive_motor(FD_1, FD_2, MOTOR_OFF);
        drive_motor(RD_1, RD_2, MOTOR_OFF);
        drive_motor(FP_1, FP_2, MOTOR_OFF);
        drive_motor(RP_1, RP_2, MOTOR_OFF);
#End rotate Definition
#
# #maybe will be added later
# def move360(double direction):
#     return

def drive_motor(pin1, pin2, power):
    if power < 0:
        robot.board.digital[pin1].write(1)
        robot.board.digital[pin2].write(0)
    else:
        robot.board.digital[pin1].write(0)
        robot.board.digital[pin2].write(1)


def rotate_arm(angle):
    robot.board[ARM_SERVO].write(angle)