import robot

LIGHT_SENSOR_PIN = 4

def is_light_on() -> bool:

    # When a bright light is detected (at least that's what this is supposed to be)
    if robot.board.analog[LIGHT_SENSOR_PIN].read() < 1000:
        return True

    return False


def run():
    if is_light_on():
        robot.state = robot.RobotState.ESCAPE_START
