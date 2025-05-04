import magneto_library
import pydexarm_Signage
import time
from pydexarm import Dexarm

MAGNETO = Dexarm(port="COM4") # the com # for MAGNETO

# initializing the dexarm
pydexarm_Signage.dexarm_init(MAGNETO)

# picking up the name tag from starting position ===== DONE =====
magneto_library.RetrievingNameTag(MAGNETO) # getting the name tag

magneto_library.PlaceToFlip(MAGNETO) # placing the name tag to the flipping mechanism

magneto_library.name_tag_flipper() # flipping the name tag

magneto_library.MagneticPickUppart1(MAGNETO) # lining up to pick up the magnet

magneto_library.mini_solenoid_ON()
magneto_library.MagneticPickUppart2(MAGNETO) # lowering down the dexarm so that the magnet can actually be picked up

magneto_library.MagneticApplication(MAGNETO)
magneto_library.mini_solenoid_OFF()

magneto_library.small_pressure(MAGNETO)

magneto_library.mini_solenoid_ON()

magneto_library.Finished(MAGNETO)

magneto_library.mini_solenoid_OFF()

