#These are the pins, meaning front/rear driver/passenger
PinFD1 = 0
PinFD2 = 1
PinFP1 = 2
PinFP2 = 3
PinRD1 = 4
PinRD2 = 5
PinRP1 = 6
PinRP2 = 7

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


def stopMotion():
    driveMotor(FD_1, FD_2, 0)
    driveMotor(RD_1, RD_2, 0)
    driveMotor(FP_1, FP_2, 0)
    driveMotor(RP_1, RP_2, 0)

#Start move8 Defintion
def move8(int direction):
    if direction == D_FORWARD: #Forward
        driveMotor(FD_1, FD_2, MOTOR_FORWARD)
        driveMotor(FP_1, FP_2, MOTOR_FORWARD)
        driveMotor(RD_1, RD_2, MOTOR_FORWARD)
        driveMotor(RP_1, RP_2, MOTOR_FORWARD)

    elif direction == D_BACKWARD:#Backward
        driveMotor(FD_1, FD_2, MOTOR_BACKWARD)
        driveMotor(FP_1, FP_2, MOTOR_BACKWARD)
        driveMotor(RD_1, RD_2, MOTOR_BACKWARD)
        driveMotor(RP_1, RP_2, MOTOR_BACKWARD)

    elif direction == D_LEFT:#Left
        driveMotor(FD_1, FD_2, MOTOR_FORWARD)
        driveMotor(FP_1, FP_2, MOTOR_BACKWARD)
        driveMotor(RD_1, RD_2, MOTOR_BACKWARD)
        driveMotor(RP_1, RP_2, MOTOR_FORWARD)

    elif direction == D_RIGHT:#Right
        driveMotor(FD_1, FD_2, MOTOR_BACKWARD)
        driveMotor(FP_1, FP_2, MOTOR_FORWARD)
        driveMotor(RD_1, RD_2, MOTOR_FORWARD)
        driveMotor(RP_1, RP_2, MOTOR_BACKWARD)

    elif direction == D_FORWARD_RIGHT:#Forward Right
        driveMotor(FD_1, FD_2, MOTOR_FORWARD)
        driveMotor(FP_1, FP_2, MOTOR_OFF)
        driveMotor(RD_1, RD_2, MOTOR_OFF)
        driveMotor(RP_1, RP_2, MOTOR_FORWARD)

    elif direction == D_FORWARD_LEFT:#Forward Left
        driveMotor(FD_1, FD_2, MOTOR_OFF)
        driveMotor(FP_1, FP_2, MOTOR_FORWARD)
        driveMotor(RD_1, RD_2, MOTOR_FORWARD)
        driveMotor(RP_1, RP_2, MOTOR_OFF)

    #NOTE I am not sure these two are correct
    elif direction == D_BACKWARD_LEFT:#Backward Left
        driveMotor(FD_1, FD_2, MOTOR_BACKWARD)
        driveMotor(FP_1, FP_2, MOTOR_OFF)
        driveMotor(RD_1, RD_2, MOTOR_OFF)
        driveMotor(RP_1, RP_2, MOTOR_BACKWARD)

    elif direction == D_BACKWARD_RIGHT: #Backward Right
        driveMotor(FD_1, FD_2, MOTOR_OFF)
        driveMotor(FP_1, FP_2, MOTOR_BACKWARD)
        driveMotor(RD_1, RD_2, MOTOR_BACKWARD)
        driveMotor(RP_1, RP_2, MOTOR_OFF)

    elif direction == D_END: #Ends Movement
        driveMotor(FD_1, FD_2, MOTOR_OFF)
        driveMotor(RD_1, RD_2, MOTOR_OFF)
        driveMotor(FP_1, FP_2, MOTOR_OFF)
        driveMotor(RP_1, RP_2, MOTOR_OFF)
#End move8 Defintion

#Start rotate Definition
def rotate(int direction):
    if direction == R_CW:
        driveMotor(FD_1, FD_2, MOTOR_FORWARD)
        driveMotor(RD_1, RD_2, MOTOR_FORWARD)
        driveMotor(FP_1, FP_2, MOTOR_BACKWARD)
        driveMotor(RP_1, RP_2, MOTOR_BACKWARD)
    elif direction ==  R_CCW:
        driveMotor(FD_1, FD_2, MOTOR_BACKWARD)
        driveMotor(RD_1, RD_2, MOTOR_BACKWARD)
        driveMotor(FP_1, FP_2, MOTOR_FORWARD)
        driveMotor(RP_1, RP_2, MOTOR_FORWARD)
    elif direction R_END:
        driveMotor(FD_1, FD_2, MOTOR_OFF);
        driveMotor(RD_1, RD_2, MOTOR_OFF);
        driveMotor(FP_1, FP_2, MOTOR_OFF);
        driveMotor(RP_1, RP_2, MOTOR_OFF);
#End rotate Definition

#maybe will be added later
def move360(double direction):
    return

def driveMotor(int pin1, int pin2, int power):
    if power < 0:
        board.digital[pin1].write(1)
        board.digital[pin2].write(0)
    else:
        board.digital[pin1].write(0)
        board.digital[pin2].write(1)
