import sys, math, time, serial
from pydexarm import Dexarm

SPEED_ROBOT = 6000
speedRobot = 6000

Z_maxheight = 50
Z_zero = 0

def name_tag_flipper():
    SERIAL_PORT = 'COM3' 
    BAUD_RATE = 115200
    TIMEOUT = 1

    serial_connection = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
    time.sleep(2)  # Allow time for the serial connection to establish
    print("Serial connection established with Arduino name tag flipping mechananism", SERIAL_PORT)

    # Command the Arduino to fli the signage measurement
    serial_connection.write(b"$S\n")

    serial_connection.close()
    print("Serial connection closed with arduino.")
    return

def mini_solenoid_ON():
    SERIAL_PORT = 'COM8' 
    BAUD_RATE = 115200
    TIMEOUT = 1

    serial_connection = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
    time.sleep(2)  # Allow time for the serial connection to establish
    print("Serial connection established with Arduino for mini solenoid", SERIAL_PORT)

    # Command the Arduino to start measurement
    serial_connection.write(b"$S\n")

    serial_connection.close()
    print("Serial connection closed with arduino.")
    return


def mini_solenoid_OFF():
    SERIAL_PORT = 'COM8' 
    BAUD_RATE = 115200
    TIMEOUT = 1

    serial_connection = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
    time.sleep(2)  # Allow time for the serial connection to establish
    print("Serial connection established with Arduino for mini solenoid", SERIAL_PORT)

    # Command the Arduino to start measurement
    serial_connection.write(b"$K\n")

    serial_connection.close()
    print("Serial connection closed with arduino.")
    return


def RetrievingNameTag(dexarm):
    dexarm.move_to(None, None, None, 853, mode = "G1", feedrate = speedRobot)
    dexarm.move_to(None, 235, Z_zero)
    dexarm.air_picker_pick()
    dexarm.move_to(None, 235, -103)
    dexarm.move_to(None, 235, Z_zero)

def PlaceToFlip(dexarm):
    dexarm.move_to(None, None, None, 240, mode = "G1", feedrate = speedRobot)
    dexarm.move_to(None, 330, Z_zero)
    dexarm.move_to(None, 330, -50, mode = "G1", feedrate = speedRobot)
    dexarm.move_to(None, 330, -70, mode = "G0", feedrate = 1000) # lowering the speed for the robot to pick up the material
    dexarm.air_picker_place()
    dexarm.move_to(None, 330, Z_maxheight)
    dexarm.air_picker_stop()
    print("$") # the name tag flips

magnet_y = 276

def MagneticPickUppart1(dexarm):
    dexarm.move_to(None, None, None, 605, mode ="G1", feedrate = speedRobot)
    dexarm.move_to(None, magnet_y, Z_zero)
    dexarm.move_to(None, magnet_y, -90)
    print("$S") # the solenoid is going up (magnet is gripping)

def MagneticPickUppart2(dexarm):
    dexarm.move_to(None, magnet_y, -100, feedrate = 1000) # makes it so that not too much pressure is applied
    dexarm.move_to(None, magnet_y, 50)

def MagneticApplication(dexarm):
    # dexarm.move_to(None, 235, Z_zero)
    # dexarm.move_to(None, None, None, 345, mode = "G0", feedrate = 3000)
    # dexarm.move_to(None, 265, Z_zero)
    # dexarm.move_to(None, 265, -110)
    dexarm.move_to(None, None, None, 345, mode = "G1", feedrate = speedRobot)
    dexarm.move_to(None, 235, 0)
    dexarm.move_to(None, 235, -90)
    print("$S") # the solenoid is going down (magnet is not longer gripping)

def small_pressure(dexarm):
    dexarm.move_to(None, None, None, 345, mode = "G1", feedrate = speedRobot)
    dexarm.move_to(None, 235, 50)
    dexarm.move_to(None, 350, 50)
    dexarm.move_to(None, 350, -110)
    dexarm.move_to(None, 350, 50)
    dexarm.move_to(None, 235, 50)
    dexarm.move_to(None, 235, -100)
    print("$")

def Finished(dexarm):
    dexarm.move_to(None, None, None, 345, mode = "G1", feedrate = speedRobot)
    dexarm.move_to(None, 235, -100)
    dexarm.move_to(None, 235, 0)
    dexarm.move_to(None, 235, 50)
    dexarm.move_to(None, None, None, 20)
    print("$")


