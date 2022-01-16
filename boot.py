# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
import setup

conf = setup.read_config("config.json")
print("Config JSON:",conf)
setup.network_connect(conf["ssid"], conf["pass"])

webrepl.start()

gc.collect()

import app