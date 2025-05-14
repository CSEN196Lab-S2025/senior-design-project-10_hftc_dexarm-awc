import nametag_lib
import time
from pydexarm import Dexarm
from alive_progress import alive_bar


magneto_arduinos = nametag_lib.NameTagArduinos()           # arduinos that control large flipper and double solenoid circuits seperately
magneto = nametag_lib.NameTagDexarm()                      # signage dexarm 

def phase1_magneto():
    magneto.air_pick()
    yield

    # initializing the dexarm 
    magneto.dexarm_init()
    yield                                      # increment progress bar - 1

    # # picking up the name tag from starting position ===== DONE =====
    magneto.retrieving_nametag()
    yield                                      # increment progress bar - 2

    # #flipping the name tag ===== DONE =====\

    magneto.place_to_flip() # placing the name tag to the flipping mechanism
    yield                                      # increment progress bar - 3

    magneto_arduinos.name_tag_flipper() # flipping the name tag
    yield                                      # increment progress bar - 4

    magneto.magnetic_pickup(magneto_arduinos) # lining up to pick up the magnet
    yield                                      # increment progress bar - 5

    magneto.magnetic_application()
    magneto_arduinos.mini_solenoid_OFF()
    yield                                      # increment progress bar - 7

    magneto.small_pressure()
    yield                                      # increment progress bar - 8

    magneto_arduinos.mini_solenoid_ON()
    time.sleep(5)
    magneto.finished()
    yield                                      # increment progress bar - 9
    
    magneto_arduinos.mini_solenoid_OFF()
    yield                                      # increment progress bar - 10


# progress bar
with alive_bar(10) as bar:
    for i in phase1_magneto():
        bar()
