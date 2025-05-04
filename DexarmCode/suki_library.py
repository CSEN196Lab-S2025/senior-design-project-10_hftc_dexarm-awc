import sys, math, time, serial
from pydexarm import Dexarm

SPEED_ROBOT = 6000
speedRobot = 6000

# create definition for the height sensor
# create definition for checking the height sensor if its valid

# this is the definition for hard-coded coordinates for the velcros and placing them on the arm
Z_maxheight = 50 # sliding rail wires are in the way
y_zero = 0
Z_zero = 0

def dexarm_init(dexarm, z = 60):
    dexarm.go_home()
    dexarm.sliding_rail_init(z)
    # time.sleep(15)

def get_sensor_height():
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

def pickStatus():
    sensor_threshold = 10
    measured_height = get_sensor_height()
    
    if measured_height < sensor_threshold:
        return True
    else:
        print(f"Sensor reading is {measured_height}mm - above missed pick threshold of {sensor_threshold}mm. Returning False.")
        return False


fast_rate = 6000
slow_rate = 1000

def SUKI_velcro(dexarm):
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
    # dexarm.go_home() # starting point
    print('-------------------------------------------move to sliding rail position')
    dexarm.move_to(e=rail_velcro, feedrate=6000,  wait=True) # the position in the slding rail for the velcros


    # # move above velcro before measuring
    # print('move to pick positions')
    dexarm.move_to(250, 0, 0, mode='G0', feedrate=6000,  wait=True)
    # # move_to(self, x=None, y=None, z=None, e=None, feedrate=2000, mode="G1", wait=True):
    # time.sleep(5)

    height = get_sensor_height() # gets the height for the distance sensor
    Z_velcro = -height
    Z_velcro_hover = Z_velcro + 10
    print('-------------------------------------------height: ', height)

    # the first velcro
            
    dexarm.air_picker_pick()
    # dexarm.move_to(245, y_zero, Z_velcro_hover,rail_velcro, mode = "G0", feedrate = fast_rate, wait=True)
    # # time.sleep(5)
    print('-------------------------------------------picking up velcro')
    dexarm.move_to(240, y_zero, Z_velcro, mode = "G0", feedrate=slow_rate, wait=True)
    # # time.sleep(5)
    dexarm.move_to(240, y_zero, Z_maxheight, wait=True)
    # # time.sleep(5)
    # # resetting the position
    dexarm.go_home()
    # # time.sleep(5)
    # first velcro application
    dexarm.move_to(-365, y_zero ,Z_maxheight, 1000, wait=True)
    # time.sleep(5)
    dexarm.move_to(-365, y_zero, Z_signage1, wait=True)
    # time.sleep(5)
    dexarm.air_picker_place()
    dexarm.move_to(-365, y_zero, Z_maxheight, wait=True)
    # time.sleep(5)

    # time.sleep(35)
    print("-------------------------------------------velcro one done")
    # resetting the position
    dexarm.go_home()
    dexarm.move_to(100,250,0)
    # the second velcro
    dexarm.move_to(290, y_zero ,Z_zero, 975)

    dexarm.air_picker_pick()
    i = Z_zero
    dexarm.move_to(290, y_zero, Z_velcro_hover,rail_velcro, mode = "G0", feedrate = fast_rate )
    dexarm.move_to(290, y_zero, Z_velcro, mode = "G0", feedrate=slow_rate)

    dexarm.move_to(290, y_zero, Z_maxheight)
    # resetting the position
    dexarm.go_home()
    # second velcro application
    dexarm.move_to(-295, y_zero, Z_zero, 1000)
    dexarm.move_to(-295, y_zero, Z_signage2)
    dexarm.air_picker_place()
    dexarm.move_to(-320, y_zero, -50)
    # time.sleep(35)
    print("-------------------------------------------velcro two done")

def SUKI_pickupSignage(dexarm):
    Z_signage = -127
    print("picking up the signage")
    dexarm.air_picker_pick()
    dexarm.move_to(None, None, None, 1000)
    # this is where the center of the signage is
    dexarm.move_to(-335, y_zero, Z_signage)
    #preparing for next step which is placing to pressure station
    dexarm.move_to(-310, y_zero, Z_maxheight)
    dexarm.go_home()
    dexarm.move_to(270, y_zero , Z_maxheight)

def SUKI_movetoPressureStation(dexarm):
    print("moving the signage to the pressure station")
    dexarm.move_to(None, None, None, 580) # this is placing down the signage
    dexarm.move_to(245, y_zero, -70)
    dexarm.air_picker_place()
    dexarm.move_to(245, y_zero, -85)
    dexarm.move_to(None, None, None, 505)

    dexarm.move_to(245, y_zero, -70) # this is the first iteration to move it right
    dexarm.move_to(None, None, None, 600)
    dexarm.air_picker_pick()
    dexarm.move_to(245, y_zero, -85)
    dexarm.move_to(None, None, None, 505)
    dexarm.air_picker_place()

    dexarm.move_to(245, y_zero, -70,) # this is the second
    dexarm.move_to(None, None, None, 580)
    dexarm.air_picker_pick()
    dexarm.move_to(245, y_zero, -85)
    dexarm.move_to(None, None, None, 505)
    dexarm.air_picker_place()

    dexarm.move_to(245, y_zero, -70) # this is getting out of the way so that the pressure station can do it's job
    dexarm.move_to(None, None, None, 580) 
    dexarm.air_picker_pick()
    dexarm.move_to(245, y_zero, -50)
    dexarm.air_picker_place()
    
    print("$S") # Pressure station task is going
    

def Finished(dexarm):
    z_finished = 100
    dexarm.air_picker_pick()
    dexarm.move_to(None, None, None, 575, mode = "G0", feedrate = speedRobot) # taking out of the signage from the pressure station
    dexarm.move_to(237, y_zero, -95)
    dexarm.move_to(237, y_zero, Z_maxheight)
    dexarm.move_to(235, y_zero, z_finished)

    dexarm.move_to(None, None, None, 30, mode = "G0", feedrate = speedRobot) # going to the finished bucket
    dexarm.move_to(None, None, 50)
    dexarm.air_picker_place()
