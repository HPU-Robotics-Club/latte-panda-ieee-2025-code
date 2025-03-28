import time
from enum import Enum
from pyfirmata import Arduino, util, SERVO
import cv2

import robot_movement as mv
from util.april_tag import AprilTagDetector


LIGHT_SENSOR_PIN = 4


class RobotState(Enum):
    WAITING = 0  # Waiting for the light to turn on
    ESCAPE_START = 1  # Move out of the starting area
    MOVE_BOX = 2  # Move boxes to the designated areas
    GATHER_OUTSIDE = 3  # Collect rocks in the outside arena
    ENTER_CAVE = 4  # Going into the cave
    GATHER_INSIDE = 5  # Collect rocks inside the cave
    EXIT_CAVE = 6  # Going out of the cave


at_detector = AprilTagDetector()
camera = cv2.VideoCapture()
state = RobotState.WAITING


def is_light_on() -> bool:

    # When a bright light is detected (at least that's what this is supposed to be)
    darkness = board.get_pin(f"a:{LIGHT_SENSOR_PIN}:i").read()
    print(f"fall into darkness... {darkness}")

    if darkness is not None and darkness < 1000:
        return True

    return False

time_start = 0

def update():
    global state

    match state:
        case RobotState.WAITING:
            if is_light_on():
                state = RobotState.ESCAPE_START
        case RobotState.ESCAPE_START:
            global time_start
            now = time.time()

            if time_start == 0:
                time_start = now
            elif now - time_start >= 1:
                move8(D_FORWARD)
            else:
                state = RobotState.MOVE_BOX
        case RobotState.MOVE_BOX:
            # states.move_box.run()
            pass
        case RobotState.GATHER_OUTSIDE:
            # states.gather_outside.run()
            pass


# Setup
board = Arduino('/dev/ttyACM0')


#These are the pins, meaning front/rear driver/passenger
FD_ENA = board.get_pin(f'a:0:o')
FD_1 = 0
FD_2 = 1
FP_ENA = board.get_pin(f'a:2:o')
FP_1 = 7
FP_2 = 8
RD_ENB = board.get_pin(f'a:1:o')
RD_1 = 2
RD_2 = 3
RP_ENB = board.get_pin(f'a:3:o')
RP_1 = 9
RP_2 = 10
ARM_SERVO = 12

board.digital[ARM_SERVO].mode = SERVO
it = util.Iterator(board)
it.start()

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
    board.analog[FD_ENA].write(speed)
    board.analog[FP_ENA].write(speed)
    board.analog[RD_ENB].write(speed)
    board.analog[RP_ENB].write(speed)

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
        drive_motor(FD_1, FD_2, MOTOR_OFF)
        drive_motor(RD_1, RD_2, MOTOR_OFF)
        drive_motor(FP_1, FP_2, MOTOR_OFF)
        drive_motor(RP_1, RP_2, MOTOR_OFF)
#End rotate Definition
#
# #maybe will be added later
# def move360(double direction):
#     return

def drive_motor(pin1, pin2, power):
    if power < 0:
        board.digital[pin1].write(1)
        board.digital[pin2].write(0)
    else:
        board.digital[pin1].write(0)
        board.digital[pin2].write(1)


def rotate_arm(angle):
    board[ARM_SERVO].write(angle)


while True:
    update()


