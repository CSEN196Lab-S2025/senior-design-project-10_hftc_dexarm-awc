import pydexarm_NameTag
import pydexarm_Signage
import time

from pydexarm import Dexarm

MAGNETO = Dexarm(port="COM4") # the com # for MAGNETO

pydexarm_Signage.dexarm_init(MAGNETO)

pydexarm_NameTag.small_pressure(MAGNETO)

pydexarm_NameTag.mini_solenoid_ON()

pydexarm_NameTag.Finished(MAGNETO)

pydexarm_NameTag.mini_solenoid_OFF()
