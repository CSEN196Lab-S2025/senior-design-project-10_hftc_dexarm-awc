import sys, math, time
import serial
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
        # Command the Arduino to be at 0 degrees
        self.ser.write(b"$H\n")
        time.sleep(5)
        print('serial buffer: ',self.ser.read_all())

    def stepperP1(self):
        # Command the Arduino to be facing the material
        self.ser.write(b"$P1\n")

    def stepperP2(self):
        # Command the Arduino to be 270 degrees
        self.ser.write(b"$P2\n")

    def stepperP3(self):
        # command the arduino to move stepper 90deg
        self.ser.write(b"$I\n")

    def get_sensor_height(self):  #Weird behavior sometimes it doesn't work
        CALIBRATION_OFFSET = 40.0

        #clear serial communication before hand # VERY IMPORTANT
        self.ser.reset_input_buffer()
        self.ser.flush()
        time.sleep(5)

        # Command the Arduino to start measurement
        print("getting measurements...")
        self.ser.write(b"$M\n")
        raw_measurement = None

        # time.sleep(10)
        # print('serial buffer: ',self.ser.read_all())

        # Wait for and process the incoming data
        while True:
            # time.sleep(0.1)
            # print("in waiting val: ", self.ser.in_waiting) ## IDK WHY THIS FUNCTION DOESN'T WORK SOMETIMES
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
        time.sleep(5)  # Allow time for the serial connection to establish
        print("Serial connection established with laser door, will OPEN DOOR now", 'COM13')

    def close_comms(self):
        self.ser.close()
        print("Serial connection closed with Arduino stepper motor.")

    def laser_door_open(self):
        # Command the Arduino to open the door
        self.ser.write(b"$S\n")
        print("Laser Door opened")

    def laser_door_close(self):
        # Command the Arduino to CLOSE the door
        self.ser.write(b"$K\n") #
        print("Laser Door closed")

class MaterialDexarm:
    def __init__(self, isNameTag):
        self.dex = Dexarm(port="COM11")
        self.isNameTag = isNameTag
        time.sleep(2)  # Allow time for the serial connection to establish
        
    # initializing the DexArm
    def dex_init(self):
        self.dex.go_home()
        self.dex.rotate_init()
        self.dex.move_to(-140, 200, 30, mode = "G0", feedrate = fast_rate)
        self.dex.move_to(x_init, y_init, z_init,mode = "G0", feedrate = fast_rate, wait = True) # these values are defined globally and can be found at the top
        time.sleep(1)
        print("========================== The dexarm for the material is initialized")        

    def air_pick(self):
        self.dex.air_picker_pick()

    # picking up the material with checkin of distance sensor
    def grab_blank_material(self, arduino):
        grab_x = x_init - 145
        grab_y = y_init
        z_max = 120 #120 # this is what they used last year

        # self.dex.move_to(-80, 250, 30, mode = "G0", feedrate = fast_rate)
        # self.dex.move_to(-70, 320, -50, mode = "G0", feedrate = fast_rate)

        self.dex.move_to(grab_x, grab_y, z_init, mode = "G0", feedrate = 3000) 
        # print(" lets see if this works * fingers crossed* ")

        height = arduino.get_sensor_height()

        time.sleep(3)
        print("========================== height: ", height)
        hover_signage = z_max - height # this is meant to make sure that the dexarm doesn't go too far down
        grab_signage = -height + 25 # this is the height to grab the material
        
        self.dex.air_picker_pick()
        self.dex.move_to(grab_x, grab_y, hover_signage, feedrate = fast_rate, wait = True) # hovering over the material
        self.dex.move_to(grab_x,grab_y, grab_signage, feedrate = fast_rate, wait = True) # grabbing the material
        self.dex.move_to(grab_x,grab_y, grab_signage+100, feedrate = fast_rate, wait = True) # lift the material
        self.dex.move_to(x_init, y_init, z_init, mode = "G0", feedrate = 3000) 
        # once the door opens the turn table will move to it's 0 angle

    # placing the material down
    def placedown_material(self):
        # will want to have the angles close to home but not really
        # there are multiple angles for smooth transition as the dexarm will use the fastest path to get to the position
        # self.dex.move_to(-200, 0, 30, None, feedrate = slow_rate, wait = True)
        # self.dex.move_to(-210, 95, 30, None, feedrate = slow_rate, wait = True)

        self.dex.move_to(-165, 165, 40, None, feedrate = fast_rate, wait = True)
        # self.dex.move_to(-140, 185, 40, None, feedrate= fast_rate, wait = True)
        self.dex.rotate_to_position(30)    # then the turn table will move ot the angle needed to pick up the material # DOUBLE CHECK!!!
        time.sleep(3)

        self.dex.move_to(0, 235, 15, None, feedrate = fast_rate, wait = True) # self.dex in front of the laser cutter
        self.dex.move_to(0, 235, 0, None, feedrate = fast_rate, wait = True)

        # the self.dex going inside of the laser cutter after this
        self.dex.move_to(-30, 340, -5, None, feedrate = fast_rate, wait = True)    
        self.dex.move_to(-30, 340, -70, None, feedrate = fast_rate, wait = True) 
        self.dex.move_to(-30, 340, - 100, None, feedrate = fast_rate, wait = True)
        self.dex.air_picker_place()
        self.dex.air_picker_stop()
        time.sleep(2)
        self.dex.move_to(-30, 340, - 80, None, feedrate = fast_rate, wait = True)

        # moving the material to a better position
        correct = 0
        for correct in range(2):
            x_corr = [5, -20, 0, 20, -40]
            y_corr = [330, 350, 360, 370]
            z_corr = [-90, -100, -110, -113, -114]

            self.dex.move_to(x_corr[0], y_corr[0], z_corr[1])
            self.dex.move_to(x_corr[0], y_corr[0], z_corr[4])
            self.dex.move_to(x_corr[0], y_corr[1], z_corr[4])
            self.dex.move_to(x_corr[0], y_corr[1], z_corr[1])

            self.dex.move_to(x_corr[1]-10, y_corr[1]-15, z_corr[1])
            self.dex.move_to(x_corr[1]-10, y_corr[1]-15, z_corr[4])
            self.dex.move_to(x_corr[1]-10, y_corr[3]-15, z_corr[4])
            self.dex.move_to(x_corr[1]-10, y_corr[3]-15, z_corr[1])

            self.dex.move_to(x_corr[2], y_corr[2], z_corr[0])
            self.dex.move_to(x_corr[2], y_corr[2], z_corr[3])
            self.dex.move_to(x_corr[4], y_corr[2], z_corr[3])
            self.dex.move_to(x_corr[4], y_corr[2], z_corr[1])

            self.dex.move_to(x_corr[3]-10, y_corr[0]+5, z_corr[0])
            self.dex.move_to(x_corr[3]-10, y_corr[0]+5, z_corr[2])
            self.dex.move_to(x_corr[4], y_corr[0]+5, z_corr[2])
            self.dex.move_to(x_corr[4], y_corr[0]+5, z_corr[1])
            

        # getting the arm outside of the laser cutter
        self.dex.move_to(0, 360, -70, None, feedrate = fast_rate, wait = True) 
        self.dex.move_to(0, 360, 0, None, feedrate = fast_rate, wait = True)
        self.dex.move_to(0, 235, 7, None, feedrate = fast_rate, wait = True)
        # self.dex.move_to(-140, 185, 40, None, feedrate= fast_rate, wait = True)
        # self.dex.move_to(-210, 95, 30, None, feedrate = slow_rate, wait = True)
        self.dex.move_to(-165, 165, 20, None, feedrate = fast_rate, wait = True)
        self.dex.move_to(-240, 0, 20, None, feedrate = fast_rate, wait = True)

        self.dex.rotate_init()
        # dexarm will go back to it's place so that it won't be in the way of the door

    # the laser cutter should run with the implemented gcode
    # door will open again

    # pick up from laser cutter
    def laser_pick_up_signage(self):
        if self.isNameTag:
            return 
        
        pick_x = -65
        pick_y = 323

        self.dex.move_to(-240, 0, 30, None, feedrate = fast_rate, wait = True)
        # self.dex.move_to(-210, 95, 30, None, feedrate = slow_rate, wait = True)

        self.dex.move_to(-165, 165, 20, None, feedrate = fast_rate, wait = True)
        # self.dex.move_to(-140, 185, 40, None, feedrate= fast_rate, wait = True)
        self.dex.move_to(0, 235, 20, None, feedrate = fast_rate, wait = True) # self.dex in front of the laser cutter

        # the self.dex going inside of the laser cutter after this
        self.dex.move_to(pick_x, pick_y, 20, None, feedrate = fast_rate, wait = True)    
        self.dex.move_to(pick_x, pick_y, -70, None, feedrate = fast_rate, wait = True) 
        self.dex.move_to(pick_x, pick_y, -127, None, feedrate = fast_rate, wait = True)
        self.dex.air_picker_pick()
        self.dex.move_to(pick_x, pick_y, -127, None, feedrate = fast_rate, wait = True)


        # getting the arm outside of the laser cutter
        self.dex.move_to(pick_x, pick_y, -70, None, feedrate = fast_rate, wait = True) 
        # self.dex.move_to(pick_x, pick_y, 0, None, feedrate = fast_rate, wait = True)
        self.dex.move_to(pick_x, pick_y, 30, None, feedrate = fast_rate, wait = True) 

        self.dex.move_to(pick_x, 235, 30, None, feedrate = fast_rate, wait = True)
        # self.dex.move_to(-140, 185, 40, None, feedrate= fast_rate, wait = True)
        # self.dex.move_to(-210, 95, 30, None, feedrate = slow_rate, wait = True)
        self.dex.rotate_to_position(20)
        self.dex.move_to(-165, 165, 30, None, feedrate = fast_rate, wait = True)
        self.dex.move_to(-235, 0, 35, None, feedrate = fast_rate, wait = True)
        # self.dex.rotate_to_position(20)

        
    def laser_pick_up_nametag(self, ind=0):
        if not self.isNameTag:
            return 

        pick_x = -30
        pick_y = [350, 320]

        self.dex.move_to(-240, 0, 30, None, feedrate = fast_rate, wait = True)
        # self.dex.move_to(-210, 95, 30, None, feedrate = slow_rate, wait = True)

        self.dex.move_to(-165, 165, 20, None, feedrate = fast_rate, wait = True)
        # self.dex.move_to(-140, 185, 40, None, feedrate= fast_rate, wait = True)
        self.dex.move_to(0, 235, 20, None, feedrate = fast_rate, wait = True) # self.dex in front of the laser cutter

        # the self.dex going inside of the laser cutter after this
        
        self.dex.move_to(pick_x, pick_y[ind], 20, None, feedrate = fast_rate, wait = True)    
        self.dex.move_to(pick_x, pick_y[ind], -70, None, feedrate = fast_rate, wait = True) 
        self.dex.move_to(pick_x, pick_y[ind], - 125, None, feedrate = fast_rate, wait = True)
        self.dex.air_picker_pick()
        self.dex.move_to(pick_x, pick_y[ind], - 125, None, feedrate = fast_rate, wait = True)


        # getting the arm outside of the laser cutter
        self.dex.move_to(pick_x, pick_y[ind], -70, None, feedrate = fast_rate, wait = True) 
        # self.dex.move_to(pick_x, pick_y[ind], 0, None, feedrate = fast_rate, wait = True)
        self.dex.move_to(pick_x, pick_y[ind], 30, None, feedrate = fast_rate, wait = True) 

        self.dex.move_to(pick_x, 235, 30, None, feedrate = fast_rate, wait = True)
        # self.dex.move_to(-140, 185, 40, None, feedrate= fast_rate, wait = True)
        # self.dex.move_to(-210, 95, 30, None, feedrate = slow_rate, wait = True)
        self.dex.move_to(-165, 165, 30, None, feedrate = fast_rate, wait = True)
        self.dex.move_to(-235, 0, 35, None, feedrate = fast_rate, wait = True)
        self.dex.rotate_to_position(20)

    def placeforqc(self):
        self.dex.move_to(-235, 0, 30, None, feedrate = fast_rate, wait = True)
        self.dex.move_to(-340, 0, 30, None, feedrate = fast_rate, wait = True)
        # needs to turn 90 degrees for the quality checking system
        self.dex.move_to(-340, 0, 0, None, feedrate = fast_rate, wait = True)
        self.dex.air_picker_place()
        self.dex.move_to(-340, 0, 30, None, feedrate = fast_rate, wait = True)
        self.dex.move_to(-235, 0, 30, None, feedrate = fast_rate, wait = True)

    # the conveyor belt moving for a while
    def conveyor(self):
        # self.dex.conveyor_belt_forward(18500)
        self.dex.conveyor_belt_move(2000, 18500)

        # self.dex.conveyor_belt_stop()

    def stopAir(self):
        self.dex.air_picker_stop()

    def pick_up_nametag(self):
        self.dex.move_to(-235, 0, 30, None, feedrate = fast_rate, wait = True)
        self.dex.move_to(-340, 0, 30, None, feedrate = fast_rate, wait = True)
        self.dex.move_to(-340, 0, -15, None, feedrate = fast_rate, wait = True)
        self.dex.air_picker_pick()
        time.sleep(1)
        self.dex.move_to(-340, 0, -15, None, feedrate = fast_rate, wait = True)
        self.dex.move_to(-340, 0, 30, None, feedrate = fast_rate, wait = True)
        self.dex.move_to(-235, 0, 30, None, feedrate = fast_rate, wait = True)
        
    # the placement for passing the name tag over
    def place_nametag(self):
        y_zero = 0
        y_placement = 220
        x_placement = -340
        z_maxheight = 50
        z_zero = 0
        z_placement = -50

        # place the rotation function here

        self.dex.move_to(-245, y_zero, z_maxheight, feedrate = fast_rate)
        self.dex.move_to(x_placement, y_placement, z_maxheight, feedrate = fast_rate)
        self.dex.move_to(x_placement, y_placement, z_zero, feedrate = fast_rate)
        self.dex.rotate_to_position(110)
        self.dex.move_to(x_placement, y_placement, z_placement, feedrate = fast_rate)
        self.dex.air_picker_place()
        self.dex.air_picker_stop()
        self.dex.move_to(x_placement, y_placement, z_placement, feedrate = fast_rate)
        self.dex.move_to(x_placement, y_placement, z_zero, feedrate = fast_rate)
        self.dex.move_to(x_placement, y_placement, z_maxheight, feedrate = fast_rate)
        self.dex.move_to(-245, y_zero, z_maxheight, feedrate = fast_rate)