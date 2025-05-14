import sys, math, time, serial
from pydexarm import Dexarm

SPEED_ROBOT = 6000
speedRobot = 6000

Z_maxheight = 50
Z_zero = 0

class NameTagArduinos:
    # Can I leave two serial ports open at once?
    def __init__(self):
        print("instance of arduino created")

    def name_tag_flipper(self):
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

    def mini_solenoid_ON(self):
        SERIAL_PORT = 'COM8' 
        BAUD_RATE = 115200
        TIMEOUT = 1

        serial_connection = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2)  # Allow time for the serial connection to establish
        print("Serial connection established with Arduino for mini solenoid", SERIAL_PORT)

        # Command the Arduino to start measurement
        serial_connection.write(b"$S\n")
        print("mini solenoid ON!!")

        serial_connection.close()
        print("Serial connection closed with arduino.")
        return

    def mini_solenoid_OFF(self):
        SERIAL_PORT = 'COM8' 
        BAUD_RATE = 115200
        TIMEOUT = 1

        serial_connection = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2)  # Allow time for the serial connection to establish
        print("Serial connection established with Arduino for mini solenoid", SERIAL_PORT)

        # Command the Arduino to start measurement
        serial_connection.write(b"$K\n")
        print("mini solenoid OFF!!")

        serial_connection.close()
        print("Serial connection closed with arduino.")
        return

class NameTagDexarm:
    magnet_y = 268

    y_offset = 40
    sr_offset = -100
    origin = [0, 268, 0, 615]
    relative_coords = [ #structured in order for pick up (only 6 of the coordinates will work)
        [0, 0], [1, 0], [2, 0],
        [0, 1], [1, 1], [2, 1],
    ]

    def __init__(self):
        self.dex = Dexarm(port="COM15")
        self.count = 0
        time.sleep(2)  # Allow time for the serial connection to establish
    
    def dexarm_init(self, z = 60):
        self.dex.go_home()
        self.dex.move_to(None, None, 50)
        self.dex.sliding_rail_init(z)
        # time.sleep(15)

    def air_pick(self):
        self.dex.air_picker_pick()
        
    def retrieving_nametag(self):
        self.dex.move_to(None, None, None, 875, mode = "G1", feedrate = speedRobot)
        self.dex.move_to(None, 250, Z_zero)
        self.dex.air_picker_pick()
        self.dex.move_to(None, 250, -103)
        self.dex.move_to(None, 250, Z_zero)

    def place_to_flip(self):
        self.dex.move_to(None, None, None, 245, mode = "G1", feedrate = speedRobot)
        self.dex.move_to(None, 345, Z_zero)
        self.dex.move_to(None, 345, -50, mode = "G1", feedrate = speedRobot)
        self.dex.move_to(None, 345, -65, mode  = "G0", feedrate = 1000) # lowering the speed for the robot to pick up the material
        self.dex.air_picker_place()
        self.dex.move_to(None, 345, Z_maxheight)
        self.dex.air_picker_stop()
        # the name tag flips

    def magnetic_pickup(self, gripper):
        m1 = NameTagDexarm.magnet_grid_position(self)
        self.dex.move_to(None, m1[1], None, m1[3], mode ="G1", feedrate = speedRobot)
        self.dex.move_to(None, m1[1], Z_zero, m1[3])
        self.dex.move_to(None, m1[1], -100, m1[3])
        
        gripper.mini_solenoid_ON() # the solenoid is going up (magnet is gripping)

        # m1 = NameTagDexarm.magnet_grid_position(self)
        self.dex.move_to(None, m1[1], -110, feedrate = 1000) # makes it so that not too much pressure is applied
        self.dex.move_to(None, m1[1], 50)


    

    def magnetic_application(self):
        # dexarm.move_to(None, 235, Z_zero)
        # dexarm.move_to(None, None, None, 345, mode = "G0", feedrate = 3000)
        # dexarm.move_to(None, 265, Z_zero)
        # dexarm.move_to(None, 265, -110)
        self.dex.move_to(None, None, None, 350, mode = "G1", feedrate = speedRobot)
        self.dex.move_to(None, 235, 0)
        self.dex.move_to(None, 235, -50)
        self.dex.move_to(None, 235, -90)
        # the solenoid is going down (magnet is not longer gripping)

    def small_pressure(self):
        self.dex.move_to(None, None, None, 350, mode = "G1", feedrate = speedRobot)
        self.dex.move_to(None, 235, 50)
        self.dex.move_to(None, 365, 50)
        self.dex.move_to(None, 365, -90)
        self.dex.move_to(None, 365, 50)
        self.dex.move_to(None, 235, 50)
        self.dex.move_to(None, 235, -50)
        self.dex.move_to(None, 235, -90)

    def finished(self):
        self.dex.move_to(None, None, None, 350, mode = "G1", feedrate = speedRobot)
        self.dex.move_to(None, 235, -90)
        self.dex.move_to(None, 235, 0)
        self.dex.move_to(None, 235, 50)
        self.dex.move_to(None, None, None, 20)

    def magnet_grid_position(self):
        x = NameTagDexarm.origin[0]
        # print('x: ', x)
        y = NameTagDexarm.origin[1]+NameTagDexarm.relative_coords[self.count][0]*NameTagDexarm.y_offset
        z = NameTagDexarm.origin[2]
        sr = NameTagDexarm.origin[3]+NameTagDexarm.relative_coords[self.count][1]*NameTagDexarm.sr_offset

        print(f'({x}, {y}, {z}, {sr})')
        self.count += 1
        return [x, y, z, sr]


