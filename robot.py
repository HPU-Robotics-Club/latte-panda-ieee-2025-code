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
    if board.analog[LIGHT_SENSOR_PIN].read() < 1000:
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
                mv.move8(mv.D_FORWARD)
            else:
                state = RobotState.MOVE_BOX
        case RobotState.MOVE_BOX:
            # states.move_box.run()
            pass
        case RobotState.GATHER_OUTSIDE:
            # states.gather_outside.run()
            pass

# Setup
board = Arduino('')
board.digital[mv.ARM_SERVO].mode = SERVO
it = util.Iterator(board)
it.start()

while True:
    update()


