
import signage_lib
import mat_lib
from pydexarm import Dexarm
import sys, math, time, serial
from alive_progress import alive_bar


sys.stdout.reconfigure(encoding='utf-8')

suki_arduinos = signage_lib.SignageArduinos()           # arduinos that control large flipper and double solenoid circuits seperately

if len(sys.argv) < 2:
    print('arg needed!')
    sys.exit()
else:
    print('arg: ', sys.argv[1])
    suki = signage_lib.SignageDexarm(int(sys.argv[1]))                      # signage dexarm 

lulu = mat_lib.MaterialDexarm(0)                         # material dexarm 

#for testing grid positions
# for i in range(8):
#     print(i)
#     print(suki.velcro_grid_position())

def phase1_signage():
    lulu.conveyor()
    yield                                      # increment progress bar - 1

    suki_arduinos.large_flipper()
    yield                                      # increment progress bar - 2

    suki.dexarm_init()  
    yield                                      # increment progress bar - 3

    # suki.stop_air()
    # Applying velcro to the backings of signage ====== DONE =======
    suki.get_velcro(suki_arduinos)
    yield                                      # increment progress bar - 4

    # move above velcro before measuring
    time.sleep(4)

    # picking up the signage ========= DONE =======
    suki.pickup_signage()
    yield                                      # increment progress bar - 5
                            
    # placing the signage into the pressure station ======= DONE =======
    suki.move_to_pressure_station()
    yield                                      # increment progress bar - 6

    suki_arduinos.double_solenoid() 
    time.sleep(5)
    yield                                      # increment progress bar - 7

    suki.finished()
    yield                                      # increment progress bar - 8

    suki.stop_air()
    yield                                      # increment progress bar - 9

# progress bar
with alive_bar(9) as bar:
    for i in phase1_signage():
        bar()


