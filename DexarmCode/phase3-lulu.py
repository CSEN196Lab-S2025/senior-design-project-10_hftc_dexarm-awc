import mat_lib
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

lulu_arduino = mat_lib.LULU_ARDUINO()          # lazy suzen & limit switch arduino
# lulu = mat_lib.MaterialDexarm()                # material dexarm 
# laser_arduino = mat_lib.Laserdoor_ARDUINO()    # laser door arduino 

def phase3():
    # lulu.air_pick()
    lulu.stopAir()
    yield                                      # increment progress bar - 1

    lulu_arduino.stepperInit()
    yield                                      # increment progress bar - 2

    lulu.dex_init()
    yield                                      # increment progress bar - 3

    lulu_arduino.stepperP2()
    yield                                      # increment progress bar - 4

    lulu.pick_up_nametag()
    yield                                      # increment progress bar - 5

    lulu_arduino.stepperP3()
    yield                                      # increment progress bar - 6

    lulu.place_nametag()
    yield                                      # increment progress bar - 7

    lulu_arduino.stepperHome()
    yield                                      # increment progress bar - 8

    lulu_arduino.close_comms()
    yield                                      # increment progress bar - 9

# progress bar
with alive_bar(9) as bar:
    for i in phase3():
        bar()

# phase3()

