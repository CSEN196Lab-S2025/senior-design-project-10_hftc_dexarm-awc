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

lulu_library.material_initialize(LULU)  # initializing the material
time.sleep(2)

l1.stepperP1()
time.sleep(2)

lulu_library.grab_blank_material(LULU, l1)

# # time.sleep(5)

# # LULU.air_picker_stop()
l1.stepperHome()
time.sleep(5)

lulu_library.placedown_material(LULU)

l1.close_comms()
