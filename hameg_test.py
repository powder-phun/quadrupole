from controllers.HamegHM5014Controller import HamegHM5014Controller
from config import Config
import time

config = Config('/home/jan/code/quadrupole/configs/HM5014.json')
print(config.controllers)

hm = HamegHM5014Controller(config.controllers[0])

hm.connect()

hm.read("Amax")