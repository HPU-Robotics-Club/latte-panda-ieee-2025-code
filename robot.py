from enum import Enum
from pyfirmata import Arduino, util, SERVO
import cv2

import robot_movement as mv
import states
from util.april_tag import AprilTagDetector


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




def update():
    match state:
        case RobotState.WAITING:
            states.waiting.run()
        case RobotState.ESCAPE_START:
            states.escape_start.run()
        case RobotState.MOVE_BOX:
            states.move_box.run()
        case RobotState.GATHER_OUTSIDE:
            states.gather_outside.run()

# Setup
board = Arduino('')
board.digital[mv.ARM_SERVO].mode = SERVO

while True:
    update()


