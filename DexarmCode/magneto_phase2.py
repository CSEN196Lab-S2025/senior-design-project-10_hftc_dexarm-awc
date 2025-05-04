import magneto_library
import suki_library
import time

from pydexarm import Dexarm

MAGNETO = Dexarm(port="COM4") # the com # for MAGNETO

suki_library.dexarm_init(MAGNETO)

magneto_library.small_pressure(MAGNETO)

magneto_library.mini_solenoid_ON()

magneto_library.Finished(MAGNETO)

magneto_library.mini_solenoid_OFF()
