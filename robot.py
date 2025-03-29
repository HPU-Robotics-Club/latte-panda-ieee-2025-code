import time
from enum import Enum
from pyfirmata import Arduino, util, SERVO
import cv2

from util.april_tag import AprilTagDetector


# Setup
print("Loading pins...")
board = Arduino('/dev/ttyACM0')

US_SENSOR_PIN = board.get_pin('a:0:i')
LIGHT_SENSOR_PIN = board.get_pin('a:4:i')


# PWM, DIR
# passengers: 3 2 12; 5 13 7
# drivers: 10 11; 8, 9:::10 8; 11 9
#These are the pins, meaning front/rear driver/passenger
FD = board.get_pin('d:8:o')
FD_PWM = board.get_pin('d:10:p')

FP_ENA = board.get_pin('d:6:p')
FP_1 = board.get_pin('d:7:o')
FP_2 = board.get_pin('d:2:o')

RD = board.get_pin('d:12:o')
RD_PWM = board.get_pin('d:9:p')

RP_ENB = board.get_pin('d:3:p')
RP_1 = board.get_pin('d:5:o')
RP_2 = board.get_pin('d:13:o')


class RobotState(Enum):
    WAITING = 0  # Waiting for the light to turn on
    ESCAPE_START = 1  # Move out of the starting area
    MOVE_BOX = 2  # Move boxes to the designated areas
    GATHER_OUTSIDE = 3  # Collect rocks in the outside arena
    ENTER_CAVE = 4  # Going into the cave
    GATHER_INSIDE = 5  # Collect rocks inside the cave
    EXIT_CAVE = 6  # Going out of the cave


print("Loading capture and april tag detector...")

at_detector = AprilTagDetector()
camera = cv2.VideoCapture()
state = RobotState.WAITING

cam_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
cam_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

def is_light_on() -> bool:
    # When a bright light is detected (at least that's what this is supposed to be)
    darkness = LIGHT_SENSOR_PIN.read()
    print(f"fall into darkness... {darkness}")

    if darkness is not None and darkness > 0.8:
        return True

    return False

time_start = 0

container_ids = [5, 6]

class CaveState(Enum):
    FINDING_TAG = 0
    IN = 1
    AND_OUT = 2

class BoxMovingState(Enum):
    FINDING_TAG = 0
    CENTERING_BOX = 1
    GO_TO_BOX = 2
    GRAB_BOX = 3
    FINDING_PAD = 4
    GO_TO_PAD = 5
    DROP_BOX = 6  # mediafire reference

class GatherState(Enum):
    SEARCHING_ROCKS = 0
    COLLECTING = 1
    SECURING = 2
    SEARCHING_BOX = 3
    GO_TO_BOX = 4
    DEPOSIT = 5

cave_tag = None
center_range = [200, 200]  # x y range
cave_enter_time = -1

cave_state = CaveState.FINDING_TAG
box_moving_state = BoxMovingState.FINDING_TAG
gather_state = GatherState.SEARCHING_ROCKS

def update():
    global state

    match state:
        case RobotState.WAITING:  # Waiting state
            if is_light_on():
                state = RobotState.ESCAPE_START

        case RobotState.ESCAPE_START:  # Escape start state
            global time_start
            now = time.time()

            if time_start == 0:
                time_start = now
            elif now - time_start < 1:
                move8(D_FORWARD)
            else:
                state = RobotState.ENTER_CAVE

        case RobotState.MOVE_BOX:  # Move box state TODO this
            global box_moving_state
            stop_motion()
            # Find april tag, find white contours (will be the containers), center, go up and grab
            img, _ = cv2.imread(camera)
            greyscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            detections = at_detector.detect_april_tags(greyscale_img)

            if len(detections) == 0:
                return

            found_container = False

            for detection in detections:
                if detection.tag_id in container_ids:
                    found_container = True
                    break

            if found_container:
                pass

            rotate_arm(40)

        case RobotState.GATHER_OUTSIDE:
            global gather_state

            match gather_state:
                case GatherState.SEARCHING_ROCKS:
                    # Get largest mass of contours. Go into the one in the center.
                    # img, _ = cv2.imread(camera)
                    # contours = mantis.find_colors()
                    pass
                case GatherState.COLLECTING:
                    dist = US_SENSOR_PIN.read()

                    if dist <= 6:
                        time.sleep(1)
                        gather_state = GatherState.SECURING
                case GatherState.SECURING:
                    rotate_arm(40)
                    gather_state = GatherState.SEARCHING_BOX
                case GatherState.SEARCHING_BOX:
                    rotate(R_CW)

                    _, img = camera.read()
                    greyscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    detections = at_detector.detect_april_tags(greyscale_img)

                    if len(detections) == 0:
                        return

                    for detection in detections:  # TODO
                        return

                case RobotState.ENTER_CAVE:
                    global cave_state
                    global cave_enter_time

                    match cave_state:
                        case CaveState.FINDING_TAG:
                            global cave_tag

                            if cave_tag is None:
                                _, img = camera.read()
                                greyscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                                detections = at_detector.detect_april_tags(greyscale_img)

                                if len(detections) == 0:
                                    return

                                for detection in detections:
                                    if detection.tag_id == 4:
                                        cave_tag = detection
                                        return

                                move8(D_LEFT)
                            else:
                                center_x, center_y = cave_tag.center
                                lower_x_bound = cam_width // 2 - center_range[0]
                                upper_x_bound = cam_width // 2 + center_range[0]
                                lower_y_bound = cam_height // 2 - center_range[1]
                                upper_y_bound = cam_height // 2 + center_range[1]

                                if lower_x_bound < center_x < upper_x_bound and lower_y_bound < center_y < upper_y_bound:
                                    stop_motion()
                                    cave_state = CaveState.IN
                                    cave_enter_time = time.time()
                        case CaveState.IN:
                            move8(D_FORWARD)

                            now = time.time()

                            if now - cave_enter_time >= 5:
                                cave_state = CaveState.AND_OUT
                                cave_enter_time = now
                        case CaveState.AND_OUT:
                            now = time.time()

                            if now - cave_enter_time >= 5:
                                state = RobotState.MOVE_BOX




ARM_SERVO = 12

board.digital[ARM_SERVO].mode = SERVO
it = util.Iterator(board)
it.start()

# Working pins
# 7, 11, 5, 2, 3, 13
# Not working
# 6, 8, 9, 10, 12
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
    drive_fd(0, 0)
    drive_fp(0, 0)
    drive_rd(0, 0)
    drive_rp(0, 0)

#Start move8 Defintion
def move8(direction):
    speed = 1.0

    if direction == D_FORWARD: #Forward
        print("vrooming forward")
        drive_fd(MOTOR_FORWARD, speed)
        drive_fp(MOTOR_FORWARD, speed)
        drive_rd(MOTOR_FORWARD, speed)
        drive_rp(MOTOR_FORWARD, speed)
    elif direction == D_BACKWARD:#Backward
        drive_fd(MOTOR_BACKWARD, speed)
        drive_fp(MOTOR_BACKWARD, speed)
        drive_rd(MOTOR_BACKWARD, speed)
        drive_rp(MOTOR_BACKWARD, speed)
    elif direction == D_LEFT:#Left
        drive_fd(MOTOR_FORWARD, speed)
        drive_fp(MOTOR_BACKWARD, speed)
        drive_rd(MOTOR_FORWARD, speed)
        drive_rp(MOTOR_BACKWARD, speed)
    elif direction == D_RIGHT:#Right
        drive_fd(MOTOR_BACKWARD, speed)
        drive_fp(MOTOR_FORWARD, speed)
        drive_rd(MOTOR_FORWARD, speed)
        drive_rp(MOTOR_BACKWARD, speed)
    elif direction == D_FORWARD_RIGHT:#Forward Right
        drive_fd(MOTOR_FORWARD, speed)
        drive_fp(MOTOR_OFF, 0)
        drive_rd(MOTOR_OFF, 0)
        drive_rp(MOTOR_FORWARD, speed)
    elif direction == D_FORWARD_LEFT:#Forward Left
        drive_fd(MOTOR_OFF, 0)
        drive_fp(MOTOR_FORWARD, speed)
        drive_rd(MOTOR_FORWARD, speed)
        drive_rp(MOTOR_OFF, 0)

    #FIXME I am not sure these two are correct
    elif direction == D_BACKWARD_LEFT:#Backward Left
        drive_fd(MOTOR_BACKWARD, speed)
        drive_fp(MOTOR_OFF, 0)
        drive_rd(MOTOR_OFF, 0)
        drive_rp(MOTOR_BACKWARD, speed)
    elif direction == D_BACKWARD_RIGHT: #Backward Right
        drive_fd(MOTOR_OFF, 0)
        drive_fp(MOTOR_BACKWARD, speed)
        drive_rd(MOTOR_BACKWARD, speed)
        drive_rp(MOTOR_OFF, 0)
    elif direction == D_END: #Ends Movement
        drive_fd(MOTOR_OFF, 0)
        drive_fp(MOTOR_OFF, 0)
        drive_rd(MOTOR_OFF, 0)
        drive_rp(MOTOR_OFF, 0)


#Start rotate Definition
def rotate(direction):
    speed = 1.0

    if direction == R_CW:
        drive_fd(MOTOR_FORWARD, speed)
        drive_fp(MOTOR_BACKWARD, speed)
        drive_rd(MOTOR_FORWARD, speed)
        drive_rp(MOTOR_BACKWARD, speed)
    elif direction ==  R_CCW:
        drive_fd(MOTOR_BACKWARD, speed)
        drive_fp(MOTOR_FORWARD, speed)
        drive_rd(MOTOR_BACKWARD, speed)
        drive_rp(MOTOR_FORWARD, speed)
    elif direction == R_END:
        drive_fd(MOTOR_OFF, 0)
        drive_fp(MOTOR_OFF, 0)
        drive_rd(MOTOR_OFF, 0)
        drive_rp(MOTOR_OFF, 0)
#End rotate Definition
#
# #maybe will be added later
# def move360(double direction):
#     return


def drive_fd(power: int, speed: float):
    if power == 1:
        power_inp = -1
    elif power == -1:
        power_inp = 1
    else:
        power_inp = 0

    drive_motor_ot(FD, FD_PWM, power_inp, speed)

def drive_fp(power: int, speed: float):
    drive_motor_en(FP_1, FP_2, FP_ENA, power, speed)

def drive_rd(power: int, speed: float):
    drive_motor_ot(RD, RD_PWM, power, speed)

def drive_rp(power: int, speed: float):
    drive_motor_en(RP_1, RP_2, RP_ENB, power, speed)


def drive_motor_en(pin1, pin2, en_pin, power: int, speed: float):
    en_pin.write(speed)

    if power < 0:
        pin1.write(1)
        pin2.write(0)
    else:
        pin1.write(0)
        pin2.write(1)


def drive_motor_ot(dir_pin, pwm_pin, power: int, speed: float):
    pwm_pin.write(speed)

    if power < 0:
        dir_pin.write(0)
    else:
        dir_pin.write(1)


def rotate_arm(angle):
    # board[ARM_SERVO].write(angle)
    pass


print("Resetting existence...")
stop_motion()

print("Let the show commence!")

while True:
    update()
    time.sleep(0.05)


