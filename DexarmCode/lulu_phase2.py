import lulu_library
from pydexarm import Dexarm
import sys, math, time, serial


sys.stdout.reconfigure(encoding='utf-8')

LULU = Dexarm(port="COM11") # the com # for SUKI

l1 = lulu_library.LULU_ARDUINO()
LULU.air_picker_stop()
# pydexarm_Material.LULU_Arduino_open_comms()
# time.sleep(3)

l1.stepperInit()
lulu_library.material_initialize(LULU)
 
l1.stepperHome()

LULU.air_picker_stop()

lulu_library.laser_pick_up(LULU)

time.sleep(5)

# pydexarm_Material.placeforqc(LULU)
LULU.air_picker_stop()

l1.close_comms()
