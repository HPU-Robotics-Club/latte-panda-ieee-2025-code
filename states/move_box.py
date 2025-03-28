import robot
import robot_movement as mv


def run():
    print("Brother, I'm cooked...")
    robot.state = robot.RobotState.GATHER_OUTSIDE
    rotate_arm(75)