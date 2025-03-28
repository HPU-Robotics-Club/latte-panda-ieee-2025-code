import time

import robot
import robot_movement as mv

time_start = 0

def run():
    global time_start
    now = time.time()

    if time_start == 0:
        time_start = now
    elif now - time_start >= 1:
        mv.move8(mv.D_FORWARD)
    else:
        robot.state = robot.RobotState.MOVE_BOX
