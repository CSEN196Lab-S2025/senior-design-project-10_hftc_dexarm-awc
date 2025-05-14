
import mat_lib                  # material picker subsystem library
from pydexarm import Dexarm
import sys, math, time, serial
from alive_progress import alive_bar


sys.stdout.reconfigure(encoding='utf-8')


if len(sys.argv) < 2:
    print('arg needed!')
    sys.exit()
else:
    print('arg: ', int(sys.argv[1]))
    lulu = mat_lib.MaterialDexarm(int(sys.argv[1]))                    

def phase1():
    lulu_arduino = mat_lib.LULU_ARDUINO()          # lazy suzen & limit switch arduino
    # lulu = mat_lib.MaterialDexarm()                # material dexarm 
    laser_arduino = mat_lib.Laserdoor_ARDUINO()    # laser door arduino 
    yield                  #increment progress bar
    
    lulu.stopAir()
    laser_arduino.laser_door_close()
    yield                  #increment progress bar

    lulu_arduino.stepperInit()
    yield                  #increment progress bar

    lulu.dex_init()  # initializing the material
    time.sleep(5)
    yield                  #increment progress bar

    lulu_arduino.stepperP1()
    time.sleep(2)
    yield                  #increment progress bar

    lulu.grab_blank_material(lulu_arduino)
    yield                  #increment progress bar
    time.sleep(5)

    ### open laser door here
    laser_arduino.laser_door_open()
    time.sleep(5)
    lulu_arduino.stepperHome()
    yield                  #increment progress bar
    # laser_arduino.laser_door_close()
    # lulu_arduino.stepperInit()
    # time.sleep(5)
    # yield                  #increment progress bar

    lulu.placedown_material() 
    yield                  #increment progress bar

    laser_arduino.laser_door_close()
    yield                  #increment progress bar

    # lulu_arduino.close_comms()
    # yield                  #increment progress bar

# progress bar
with alive_bar() as bar:
    for i in phase1():
        bar()

# phase1()








# # stepper motor position tests
# lulu_arduino.stepperHome()
# time.sleep(5)
# lulu_arduino.stepperInit()
# time.sleep(5)
# lulu_arduino.stepperP1()
# time.sleep(5)
# lulu_arduino.stepperP2()
# time.sleep(5)