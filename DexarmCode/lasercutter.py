import serial
import time
import sys
import os
from alive_progress import alive_bar
import mat_lib                  # material picker subsystem library

baud_rate = 115200
port = 'COM10'
filename = None
ser = None
laser_arduino = mat_lib.Laserdoor_ARDUINO()    # laser door arduino 

def connect_to_lasercutter():
    global ser
    try:
        ser = serial.Serial(port, baud_rate)
        print(f"Connected to {port} at {baud_rate} baud")
        time.sleep(5)
        ser.flushInput()  # Clear startup garbage
    except serial.SerialException as e:
        print(f"Error connecting to serial port: {e}")
        exit()

def send_gcode(command):
    if ser is None:
        print('Serial not connected!')
        return
    ser.write((command + '\n').encode())
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    print(f"Sent: {command}, Received: {response}")

def main():
    send_gcode('$H')  # Home the laser cutter
    print('lasercutter homed')
    time.sleep(1)

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        with alive_bar(len(lines)) as bar:
            for line in lines:
                send_gcode(line.strip())
                bar()
    except FileNotFoundError:
        print(f"Error: G-code file '{filename}' not found.")
    finally:
        if ser:
            ser.write(('G0 X0Y400 ' + '\n').encode()) #move laser cutter out of the way
            time.sleep(3)
            ser.close()
            print("Serial connection closed.")
        print("Laser Cutter Done!")

    send_gcode('G0 X0Y400')  # move the laser cutter away
    print('lasercutter out of way')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <gcode_filename>")
        sys.exit(1)

    filename = sys.argv[1]
    print('Filename:', filename)

    connect_to_lasercutter()
    main()

## light burn setting will be remembered and affect lasercutter positioning
## $H  ; VERY IMPORTANT (AT TOP OF GCODE FILE) - This makes sure that the laser cutter is homed
## G0 X0Y400 ; VERY IMPORTANT (AT BOTTOM OF GCODE FILE) - this makes sure that the laser will move away so the door won't interfere