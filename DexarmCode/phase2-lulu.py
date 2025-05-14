import mat_lib
from pydexarm import Dexarm
import sys, math, time, serial
from alive_progress import alive_bar


sys.stdout.reconfigure(encoding='utf-8')

itemNum = 0

if len(sys.argv) < 2:
    print('arg needed!')
    sys.exit()
else:
    print('arg: ', int(sys.argv[1]))
    b = int(sys.argv[1])
    
    # itemNum = int(sys.argv[2])
    # if b not in (0, 1):
    #     print('arg value should be 1 or 0')
    #     sys.exit()
    # else:
    lulu = mat_lib.MaterialDexarm(int(sys.argv[1]))                      


lulu_arduino = mat_lib.LULU_ARDUINO()          # lazy suzen & limit switch arduino
# lulu = mat_lib.MaterialDexarm()                # material dexarm 
laser_arduino = mat_lib.Laserdoor_ARDUINO()    # laser door arduino 

def phase2():
    lulu.stopAir()
    yield                                      # increment progress bar - 1

    lulu_arduino.stepperInit()
    yield                                      # increment progress bar - 2

    lulu.dex_init()
    yield                                      # increment progress bar - 3
    
    lulu_arduino.stepperHome()
    yield                                      # increment progress bar - 4

    laser_arduino.laser_door_open()
    yield                                      # increment progress bar - 5

    # only one of these functions will run
    lulu.laser_pick_up_signage()
    lulu.laser_pick_up_nametag(itemNum)
    time.sleep(5)
    yield                                      # increment progress bar - 6

    laser_arduino.laser_door_close()
    yield                                      # increment progress bar - 7

    lulu_arduino.stepperP2()
    time.sleep(5)
    yield                                      # increment progress bar - 8

    lulu.placeforqc()
    yield                                      # increment progress bar - 9

    lulu.stopAir()
    yield                                      # increment progress bar - 10

    lulu_arduino.stepperInit
    yield                                      # increment progress bar - 11

    lulu_arduino.close_comms()
    yield                                      # increment progress bar - 12

# progress bar
with alive_bar(12) as bar:
    for i in phase2():
        bar()

# phase2()

