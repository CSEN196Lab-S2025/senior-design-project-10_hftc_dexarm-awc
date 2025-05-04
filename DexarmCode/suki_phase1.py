
import suki_library
from pydexarm import Dexarm
import sys, math, time, serial

sys.stdout.reconfigure(encoding='utf-8')


SUKI = Dexarm(port="COM19") # the com # for SUKI 
suki_library.dexarm_init(SUKI) 
# # time.sleep(20)
# # Applying velcro to the backings of signage ====== DONE =======
suki_library.SUKI_velcro(SUKI)

# # picking up the signage ========= DONE =======
suki_library.SUKI_pickupSignage(SUKI)
                          
# # # placing the signage into the pressure station ======= DONE =======
suki_library.SUKI_movetoPressureStation(SUKI)

