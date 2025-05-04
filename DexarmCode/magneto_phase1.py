import pydexarm_NameTag
import pydexarm_Signage
import time
from pydexarm import Dexarm

MAGNETO = Dexarm(port="COM4") # the com # for MAGNETO

# initializing the dexarm
pydexarm_Signage.dexarm_init(MAGNETO)

# picking up the name tag from starting position ===== DONE =====
pydexarm_NameTag.RetrievingNameTag(MAGNETO) # getting the name tag

pydexarm_NameTag.PlaceToFlip(MAGNETO) # placing the name tag to the flipping mechanism

pydexarm_NameTag.name_tag_flipper() # flipping the name tag

pydexarm_NameTag.MagneticPickUppart1(MAGNETO) # lining up to pick up the magnet

pydexarm_NameTag.mini_solenoid_ON()
pydexarm_NameTag.MagneticPickUppart2(MAGNETO) # lowering down the dexarm so that the magnet can actually be picked up

pydexarm_NameTag.MagneticApplication(MAGNETO)
pydexarm_NameTag.mini_solenoid_OFF()

pydexarm_NameTag.small_pressure(MAGNETO)

pydexarm_NameTag.mini_solenoid_ON()

pydexarm_NameTag.Finished(MAGNETO)

pydexarm_NameTag.mini_solenoid_OFF()

