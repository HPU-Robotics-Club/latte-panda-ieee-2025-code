import time

import cv2

import robot
import robot_movement as mv
from enum import Enum

US_SENSOR_PIN = 10


class GatherState(Enum):
    SEARCHING_ROCKS = 0
    COLLECTING = 1
    SECURING = 2
    SEARCHING_BOX = 3
    GO_TO_BOX = 4
    DEPOSIT = 5


state = GatherState.SEARCHING_ROCKS


def run():
    global state

    match state:
        case GatherState.SEARCHING_ROCKS:
            pass
        case GatherState.COLLECTING:
            dist = robot.board.analog[US_SENSOR_PIN].read()

            if dist <= 6:
                time.sleep(1)
                state = GatherState.SECURING
        case GatherState.SECURING:
            rotate_arm(40)
            state = GatherState.SEARCHING_BOX
        case GatherState.SEARCHING_BOX:
            rotate(R_CW)

            img, _ = cv2.imread(robot.camera)
            greyscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            detections = robot.at_detector.detect_april_tags(greyscale_img)

            if len(detections) == 0:
                return

            for detection in detections:  # TODO
                return

