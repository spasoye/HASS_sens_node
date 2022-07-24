# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
import setup
import sys

sys.path.append('/libs')
sys.path.append('/')

conf = setup.read_config("config.json")
print("Config JSON:",conf)
setup.network_connect(conf["ssid"], conf["pass"])

webrepl.start()

gc.collect()

# import app
import app_bme
app_bme.main()