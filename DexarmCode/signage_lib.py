import sys, math, time, serial
from pydexarm import Dexarm

# SPEED_ROBOT = 6000
# speedRobot = 6000

# create definition for the height sensor
# create definition for checking the height sensor if its valid

# this is the definition for hard-coded coordinates for the velcros and placing them on the arm

class SignageArduinos:
    def large_flipper(self):
        SERIAL_PORT = 'COM25' 
        BAUD_RATE = 115200
        TIMEOUT = 1

        serial_connection = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2)  # Allow time for the serial connection to establish
        print("Serial connection established with Arduino for large flipper", SERIAL_PORT)

        # Command the Arduino to start measurement
        serial_connection.write(b"$S\n")

        serial_connection.close()
        print("Serial connection closed with arduino.")

    def double_solenoid(self):
        SERIAL_PORT = 'COM22' 
        BAUD_RATE = 115200
        TIMEOUT = 1

        serial_connection = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2)  # Allow time for the serial connection to establish
        print("Serial connection established with Arduino for double solenoid", SERIAL_PORT)

        # Command the Arduino to start measurement
        serial_connection.write(b"$S\n")

        serial_connection.close()
        print("Serial connection closed with arduino.")
        return

    def get_sensor_height(self):
        SERIAL_PORT = 'COM24' 
        BAUD_RATE = 115200
        TIMEOUT = 1
        CALIBRATION_OFFSET = 40.0

        serial_connection = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2)  # Allow time for the serial connection to establish
        print("Serial connection established with TOF Sensor on", SERIAL_PORT)

        # Command the Arduino to start measurement
        serial_connection.write(b"$M\n")
        raw_measurement = None

        # Wait for and process the incoming data
        while True:
            if serial_connection.in_waiting > 0:
                line = serial_connection.readline().decode().strip()
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

        serial_connection.close()
        print("Serial connection closed with TOF Sensor.")
        return calibrated_measurement

    def pickStatus(self):
        sensor_threshold = 10
        measured_height = SignageArduinos.get_sensor_height()
        
        if measured_height < sensor_threshold:
            return True
        else:
            print(f"Sensor reading is {measured_height}mm - above missed pick threshold of {sensor_threshold}mm. Returning False.")
            return False


class SignageDexarm:
    fast_rate = 6000
    slow_rate = 1000
    Z_maxheight = 50 # sliding rail wires are in the way
    y_zero = 0
    Z_zero = 0

    x_offset = 48
    sr_offset = -100
    origin = [242, 0, 0, 975]
    relative_coords = [ #structured in order for pick up
        [0, 0], [1, 0], [2, 0],
        [0, 1], [1, 1], [2, 1],
        [0, 2], [1, 2], [2, 2],
    ]

    def __init__(self, count):
        self.dex = Dexarm(port="COM19")
        time.sleep(2)  # Allow time for the serial connection to establish

        if(count > 0 and count < 8):
            self.count = count
        else:
            print('count value not recoginzed. please try again.')
            
    def dexarm_init(self, z = 60):
        self.dex.go_home()
        self.dex.move_to(None, None, 50)
        self.dex.sliding_rail_init(z)
        # time.sleep(15)

    def stop_air(self):
        self.dex.air_picker_stop()

    def get_velcro(self, arduino):
        # print("If next year could find a better way to do this, that would be amazing")
        print("-------------------------------------------applying the velcros")

        #Z_velcro = -85 # this is the height at which the dexarm has to be to grab the velcro
        Z_signage1 = -117 # the height for the first velcro to be applied
        Z_signage2 = -119 # the height for the second velcro to be applied

        y_reset = 270

        rail_velcro = 975 # this is the position in the sliding rail to grab the velcros
        rail_signage = 1000 # this is sliding rail position for dexarm to apply velcros

        # right now just manually putting in the coordinates; will improve on this later
        # print('go home')
        # self.dex.go_home() # starting point
        print('-------------------------------------------move to sliding rail position')
        self.dex.move_to(e=rail_velcro, feedrate=6000,  wait=True) # the position in the slding rail for the velcros


        # # move above velcro before measuring
        # print('move to pick positions')
        self.dex.move_to(250, 0, 0, mode='G0', feedrate=6000,  wait=True)
        # # move_to(self, x=None, y=None, z=None, e=None, feedrate=2000, mode="G1", wait=True):
        # time.sleep(5)

        height = arduino.get_sensor_height() # gets the height for the distance sensor
        Z_velcro = -height
        Z_velcro_hover = Z_velcro + 10
        print('-------------------------------------------height: ', height)

        velcro_app_positions = [-363,-295]

        # the first velcro
        for i in range(2):
            
            self.dex.air_picker_pick()
            print('-------------------------------------------picking up velcro')
            v1 = SignageDexarm.velcro_grid_position(self)
            self.dex.move_to(None, None, None, v1[3], mode = "G1", feedrate = SignageDexarm.fast_rate, wait=True)
            self.dex.move_to(v1[0], v1[1], SignageDexarm.Z_zero, v1[3], mode = "G0", feedrate=SignageDexarm.slow_rate, wait=True)
            self.dex.move_to(v1[0], v1[1], Z_velcro, v1[3], mode = "G0", feedrate=SignageDexarm.slow_rate, wait=True)
            time.sleep(2)
            self.dex.move_to(v1[0], v1[1], SignageDexarm.Z_maxheight, v1[3], mode = "G0", feedrate=SignageDexarm.slow_rate, wait=True)

            # # resetting the position
            self.dex.go_home()
            # first velcro application
            self.dex.move_to(velcro_app_positions[i], SignageDexarm.y_zero ,SignageDexarm.Z_maxheight, 1000, wait=True)
            self.dex.move_to(velcro_app_positions[i], SignageDexarm.y_zero, Z_signage1, wait=True)
            self.dex.air_picker_place()
            self.dex.move_to(velcro_app_positions[i], SignageDexarm.y_zero, SignageDexarm.Z_maxheight, wait=True)
            print(f"-------------------------------------------velcro {i} done")
            
            if i != 1:
                # resetting the position
                self.dex.go_home()
                self.dex.move_to(100,250,0)
                self.dex.move_to(250,0,0)

        self.dex.move_to(-335, 0, 50)

    def pickup_signage(self):
        Z_signage = -127
        print("picking up the signage")
        self.dex.air_picker_pick()
        self.dex.move_to(None, None, None, 1000)
        # this is where the center of the signage is
        self.dex.move_to(-335, SignageDexarm.y_zero, Z_signage)
        #preparing for next step which is placing to pressure station
        self.dex.move_to(-310, SignageDexarm.y_zero, SignageDexarm.Z_maxheight)
        self.dex.go_home()
        self.dex.move_to(270, SignageDexarm.y_zero , SignageDexarm.Z_maxheight)

    def move_to_pressure_station(self):
        print("moving the signage to the pressure station")
        self.dex.move_to(None, None, None, 580) # this is placing down the signage
        self.dex.move_to(245, SignageDexarm.y_zero, -70)
        self.dex.air_picker_place()
        self.dex.move_to(245, SignageDexarm.y_zero, -85)
        self.dex.move_to(None, None, None, 505)

        self.dex.move_to(245, SignageDexarm.y_zero, -70) # this is the first iteration to move it right
        self.dex.move_to(None, None, None, 600)
        self.dex.air_picker_pick()
        self.dex.move_to(245, SignageDexarm.y_zero, -85)
        self.dex.move_to(None, None, None, 505)
        self.dex.air_picker_place()

        self.dex.move_to(245, SignageDexarm.y_zero, -70,) # this is the second
        self.dex.move_to(None, None, None, 580)
        self.dex.air_picker_pick()
        self.dex.move_to(245, SignageDexarm.y_zero, -85)
        self.dex.move_to(None, None, None, 505)
        self.dex.air_picker_place()

        self.dex.move_to(245, SignageDexarm.y_zero, -70) # this is getting out of the way so that the pressure station can do it's job
        self.dex.move_to(None, None, None, 580) 
        self.dex.air_picker_pick()
        self.dex.move_to(245, SignageDexarm.y_zero, -50)
        self.dex.air_picker_place()
        
    def finished(self):
        z_finished = 100
        # height = get_sensor_height()
        z_pick_up = -87
        self.dex.air_picker_pick()
        self.dex.move_to(None, None, None, 575, mode = "G0", feedrate = SignageDexarm.fast_rate) # taking out of the signage from the pressure station
        self.dex.move_to(239, SignageDexarm.y_zero, z_pick_up)
        self.dex.move_to(239, SignageDexarm.y_zero, SignageDexarm.Z_maxheight)
        self.dex.move_to(235, SignageDexarm.y_zero, z_finished)

        self.dex.move_to(None, None, None, 30, mode = "G0", feedrate = SignageDexarm.fast_rate) # going to the finished bucket
        self.dex.move_to(None, None, 50)
        self.dex.air_picker_place()

    def velcro_grid_position(self):
        self.count += 1
        x = SignageDexarm.origin[0]+SignageDexarm.relative_coords[self.count][0]*SignageDexarm.x_offset
        # print('x: ', x)
        y = SignageDexarm.origin[1]
        z = SignageDexarm.origin[2]
        sr = SignageDexarm.origin[3]+SignageDexarm.relative_coords[self.count][1]*SignageDexarm.sr_offset

        print(f'({x}, {y}, {z}, {sr})')
        return [x, y, z, sr] 
    


        relative_coords = [ #structured in order for pick up

        [0, 0], [1, 0], [2, 0],
        [0, 1], [1, 1], [2, 1],
        [0, 2], [1, 2], [2, 2],
    ]