import sys, math, time, serial
from pydexarm import Dexarm

serial_connection = None
ARDUINO_PORT = 'COM7'
SPEED_ROBOT = 6000
speedRobot = 6000

x_init = -240
y_init = 0
z_init = 30 
fast_rate = 6000
slow_rate = 1000


class LULU_ARDUINO:
    # important note, when setting up the dexarm make sure to have 
    # the button to turn on the dexarm facing towards the conveyor belt
    # then move dexarm to th

    def __init__(self):
        self.ser = serial.Serial(ARDUINO_PORT, baudrate=115200, timeout=1)
        time.sleep(2)  # Allow time for the serial connection to establish
        print("Serial connection established with Arduino for LULU", ARDUINO_PORT)

    def close_comms(self):
        self.ser.close()
        print("Serial connection closed with Arduino stepper motor.")

    def stepperInit(self): # this function inits stepper w/ home then sends it to 90deg angle so dexarm has room to init
        # Command the Arduino to initialize stepper motor
        self.ser.write(b"$H\n")
        time.sleep(4)
        # Command the Arduino to move stepper to 90deg
        self.ser.write(b"$I\n")

    def stepperHome(self):  # this function inits home position then sets dexarm platform parallel to laser door
        # Command the Arduino to start measurement
        self.ser.write(b"$H\n")

    def stepperP1(self):
        # Command the Arduino to start measurement
        self.ser.write(b"$P1\n")

    def stepperP2(self):
        # Command the Arduino to start measurement
        self.ser.write(b"$P2\n")

    def get_sensor_height(self):  #Weird behavior sometimes it doesn't work
        CALIBRATION_OFFSET = 40.0

        #clear serial communication before hand # VERY IMPORTANT
        self.ser.flush()
        time.sleep(5)

        # Command the Arduino to start measurement
        print("getting measurements...")
        self.ser.write(b"$M\n")
        raw_measurement = None

        # Wait for and process the incoming data
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode().strip()
                print("line: ", line)
                if line.startswith("$M"):
                    # Parse the average distance measurement
                    raw_measurement = float(line[2:])
                elif line == "$D":
                    # End of measurement data transmission
                    break

        if raw_measurement is None:
            print("Measurement error or no data received.")
            return None

        # Apply the calibration offset and round the result
        calibrated_measurement = round(raw_measurement - CALIBRATION_OFFSET, 1)

        # Debug message
        print(f"Debug Info: Raw measurement = {raw_measurement} mm, "
            f"Calibrated measurement = {calibrated_measurement} mm, "
            f"Current offset = {CALIBRATION_OFFSET} mm")

        return calibrated_measurement

class Laserdoor_ARDUINO:
    def __init__(self):
        self.ser = serial.Serial('COM13', baudrate=115200, timeout=1)
        time.sleep(2)  # Allow time for the serial connection to establish
        print("Serial connection established with laser door, will OPEN DOOR now", 'COM13')

    def close_comms(self):
        self.ser.close()
        print("Serial connection closed with Arduino stepper motor.")

    def laser_door_open():
        # Command the Arduino to open the door
        serial_connection.write(b"$S\n")
        print("Laser Door opened")

    def laser_door_close():
        # Command the Arduino to CLOSE the door
        serial_connection.write(b"$K\n") #
        print("Laser Door closed")

# initializing the DexArm
def material_initialize(dexarm):
    dexarm.go_home()
    dexarm.rotate_init()
    dexarm.move_to(-140, 200, 30, mode = "G0", feedrate = fast_rate)
    dexarm.move_to(x_init, y_init, z_init,mode = "G0", feedrate = fast_rate, wait = True) # these values are defined globally and can be found at the top
    time.sleep(5)
    print("========================== The dexarm for the material is initialized")
    # print("$") # this is the function for the turn table to initialize itself
    
# then the turn table will move ot the angle needed to pick up the material

def rotate_first(dexarm):
    dexarm.rotate_to_position(30)

# picking up the material with checkin of distance sensor
def grab_blank_material(dexarm, arduino):
    grab_x = x_init - 152
    grab_y = y_init
    z_max = 120 #120 # this is what they used last year

    # dexarm.move_to(-80, 250, 30, mode = "G0", feedrate = fast_rate)
    # dexarm.move_to(-70, 320, -50, mode = "G0", feedrate = fast_rate)

    dexarm.move_to(grab_x, grab_y, z_init, mode = "G0", feedrate = 3000) 
    # print(" lets see if this works * fingers crossed* ")

    height = arduino.get_sensor_height()

    time.sleep(3)
    print("========================== height: ", height)
    hover_signage = z_max - height # this is meant to make sure that the dexarm doesn't go too far down
    grab_signage = -height + 25 # this is the height to grab the material
    
    dexarm.air_picker_pick()
    dexarm.move_to(grab_x, grab_y, hover_signage, feedrate = fast_rate, wait = True) # hovering over the material
    dexarm.move_to(grab_x,grab_y, grab_signage, feedrate = fast_rate, wait = True) # grabbing the material
    dexarm.move_to(grab_x,grab_y, grab_signage+100, feedrate = fast_rate, wait = True) # lift the material
    dexarm.move_to(x_init, y_init, z_init, mode = "G0", feedrate = 3000) 
    print("$") # this is meant to open the door

# once the door opens the turn table will move to it's 0 angle

# placing the material down
def placedown_material(dexarm):
    # will want to have the angles close to home but not really
    # there are multiple angles for smooth transition as the dexarm will use the fastest path to get to the position
    # dexarm.move_to(-200, 0, 30, None, feedrate = slow_rate, wait = True)
    # dexarm.move_to(-210, 95, 30, None, feedrate = slow_rate, wait = True)

    dexarm.move_to(-165, 165, 40, None, feedrate = fast_rate, wait = True)
    # dexarm.move_to(-140, 185, 40, None, feedrate= fast_rate, wait = True)
    rotate_first(dexarm)
    time.sleep(3)

    dexarm.move_to(0, 235, 15, None, feedrate = fast_rate, wait = True) # dexarm in front of the laser cutter
    dexarm.move_to(0, 235, 0, None, feedrate = fast_rate, wait = True)

    # the dexarm going inside of the laser cutter after this
    dexarm.move_to(-30, 335, -5, None, feedrate = fast_rate, wait = True)    
    dexarm.move_to(-30, 335, -70, None, feedrate = fast_rate, wait = True) 
    dexarm.move_to(-30, 335, - 100, None, feedrate = fast_rate, wait = True)
    dexarm.air_picker_place()
    dexarm.air_picker_stop()
    time.sleep(2)
    dexarm.move_to(-30, 335, - 80, None, feedrate = fast_rate, wait = True)

    # moving the material to a better position
    correct = 0
    for correct in range(2):
        x_corr = [5, -20, 0, 20, -40]
        y_corr = [330, 350, 360, 370]
        z_corr = [-90, -100, -110, -113, -114]

        dexarm.move_to(x_corr[0], y_corr[0], z_corr[1])
        dexarm.move_to(x_corr[0], y_corr[0], z_corr[4])
        dexarm.move_to(x_corr[0], y_corr[1], z_corr[4])
        dexarm.move_to(x_corr[0], y_corr[1], z_corr[1])

        dexarm.move_to(x_corr[1]-10, y_corr[1]-15, z_corr[1])
        dexarm.move_to(x_corr[1]-10, y_corr[1]-15, z_corr[4])
        dexarm.move_to(x_corr[1]-10, y_corr[3]-15, z_corr[4])
        dexarm.move_to(x_corr[1]-10, y_corr[3]-15, z_corr[1])

        dexarm.move_to(x_corr[2], y_corr[2], z_corr[0])
        dexarm.move_to(x_corr[2], y_corr[2], z_corr[3])
        dexarm.move_to(x_corr[4], y_corr[2], z_corr[3])
        dexarm.move_to(x_corr[4], y_corr[2], z_corr[1])

        dexarm.move_to(x_corr[3]-10, y_corr[0]+5, z_corr[0])
        dexarm.move_to(x_corr[3]-10, y_corr[0]+5, z_corr[2])
        dexarm.move_to(x_corr[4], y_corr[0]+5, z_corr[2])
        dexarm.move_to(x_corr[4], y_corr[0]+5, z_corr[1])
        

    # getting the arm outside of the laser cutter
    dexarm.move_to(0, 360, -70, None, feedrate = fast_rate, wait = True) 
    dexarm.move_to(0, 360, 0, None, feedrate = fast_rate, wait = True)
    dexarm.move_to(0, 235, 7, None, feedrate = fast_rate, wait = True)
    # dexarm.move_to(-140, 185, 40, None, feedrate= fast_rate, wait = True)
    # dexarm.move_to(-210, 95, 30, None, feedrate = slow_rate, wait = True)
    dexarm.move_to(-165, 165, 20, None, feedrate = fast_rate, wait = True)
    dexarm.move_to(-240, 0, 20, None, feedrate = fast_rate, wait = True)

    dexarm.rotate_init()

    # dexarm will go back to it's place so that it won't be in the way of the door
    print("$") # this is meant to close the door after

# the laser cutter should run with the implemented gcode
# door will open again

# pick up from laser cutter
def laser_pick_up(dexarm):
    
    pick_x = -60
    pick_y = 340

    dexarm.move_to(-240, 0, 30, None, feedrate = fast_rate, wait = True)
    # dexarm.move_to(-210, 95, 30, None, feedrate = slow_rate, wait = True)

    dexarm.move_to(-165, 165, 20, None, feedrate = fast_rate, wait = True)
    # dexarm.move_to(-140, 185, 40, None, feedrate= fast_rate, wait = True)
    dexarm.move_to(0, 235, 20, None, feedrate = fast_rate, wait = True) # dexarm in front of the laser cutter

    # the dexarm going inside of the laser cutter after this
    dexarm.move_to(pick_x, pick_y, 20, None, feedrate = fast_rate, wait = True)    
    dexarm.move_to(pick_x, pick_y, -70, None, feedrate = fast_rate, wait = True) 
    dexarm.move_to(pick_x, pick_y, - 110, None, feedrate = fast_rate, wait = True)
    dexarm.air_picker_pick()
    dexarm.move_to(pick_x, pick_y, - 110, None, feedrate = fast_rate, wait = True)


    # getting the arm outside of the laser cutter
    dexarm.move_to(pick_x, pick_y, -70, None, feedrate = fast_rate, wait = True) 
    # dexarm.move_to(pick_x, pick_y, 0, None, feedrate = fast_rate, wait = True)
    dexarm.move_to(pick_x, pick_y, 30, None, feedrate = fast_rate, wait = True) 

    dexarm.move_to(pick_x, 235, 30, None, feedrate = fast_rate, wait = True)
    # dexarm.move_to(-140, 185, 40, None, feedrate= fast_rate, wait = True)
    # dexarm.move_to(-210, 95, 30, None, feedrate = slow_rate, wait = True)
    dexarm.move_to(-165, 165, 30, None, feedrate = fast_rate, wait = True)
    dexarm.move_to(-235, 0, 35, None, feedrate = fast_rate, wait = True)
    print("$") # this is the command so that the turn table will move 180 degrees


def placeforqc(dexarm):
    dexarm.move_to(-235, 0, 30, None, feedrate = fast_rate, wait = True)
    dexarm.move_to(-330, 0, 30, None, feedrate = fast_rate, wait = True)
    dexarm.move_to(-330, 0, -50, None, feedrate = fast_rate, wait = True)
    dexarm.air_picker_place()
    dexarm.move_to(-330, 0, 30, None, feedrate = fast_rate, wait = True)
    dexarm.move_to(-235, 0, 30, None, feedrate = fast_rate, wait = True)


# the conveyor belt moving for a while
def conveyor(dexarm):
    dexarm.conveyor_belt_move(2000, 15000)

# the placement for passing the name tag over
def place_nametag(dexarm):
    y_zero = 0
    z_maxheight = 50
    z_zero = 0
    z_placement = -80
    dexarm.move_to(-245, y_zero, z_maxheight, feedrate = fast_rate)
    dexarm.move_to(-380, y_zero, z_maxheight, feedrate = fast_rate)
    dexarm.move_to(-380, y_zero, z_zero, feedrate = fast_rate)
    dexarm.rotate_to_position(45)
    dexarm.move_to(-380, y_zero, z_placement, feedrate = fast_rate)
    dexarm.air_picker_place()
    dexarm.air_picker_stop()
    dexarm.move_to(-380, y_zero, z_placement, feedrate = fast_rate)
    dexarm.move_to(-380, y_zero, z_zero, feedrate = fast_rate)
    dexarm.move_to(-380, y_zero, z_maxheight, feedrate = fast_rate)
    dexarm.move_to(-245, y_zero, z_maxheight, feedrate = fast_rate)
