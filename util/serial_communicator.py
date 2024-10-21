import math

import serial

DIVIDER = "|"


class SerialCommunicator:
    def __init__(self, port: str, baud_rate: int):
        # self.arduino = serial.Serial(port, baud_rate)
        print("Starting serial communicator...")

    def write(self, msg: str):
        code = f'{msg}{DIVIDER}'
        # self.arduino.write(code.encode())
        print(f'{code}')

    def write_motor_cmd(self, motor_code: str, value: int):
        if not -255 <= value <= 255:
            raise ValueError(f"Motor command value should be in between -255 and 255.\nActual: {value}")

        sign = '-' if value < 0 else '+'
        code = motor_code + sign
        abs_value = abs(value)

        digits = int(math.log10(abs_value)) + 1

        if digits < 3:
            code += '0' * (3 - digits)  # Ensures the string is 3 digits by adding missing zeros in the beginning of the string.
        elif digits > 3:
            raise ValueError("Motor command value is longer than 3 digits.")

        code += str(abs_value)

        self.write(code)


# make sure that there is an "rf" then there will be an "f" or "b" for front or back then the following three charcters will be an number between  -255 to 255(6 charcters in each of the motor codes)
# have unassigned values
class MotorCode:
    RIGHT_FRONT_WHEEL = "rf"
    RIGHT_BACK_WHEEL = "rb"
    LEFT_FRONT_WHEEL = "lf"
    LEFT_BACK_WHEEL = "lb"


if __name__ == "__main__":
    s_com = SerialCommunicator("hi", 2)
    s_com.write_motor_cmd(MotorCode.RIGHT_BACK_WHEEL,103)
    s_com.write_motor_cmd(MotorCode.LEFT_BACK_WHEEL, 3)
    s_com.write_motor_cmd(MotorCode.RIGHT_FRONT_WHEEL, -32)
    s_com.write_motor_cmd(MotorCode.LEFT_FRONT_WHEEL, 344)
