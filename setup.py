import ujson
import network

def network_connect(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    
    print("NETWORK SETUP")
    
    if not sta_if.isconnected():
        print('connecting to network: ', ssid )
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def read_config(file):
    cfg_file = open(file, "r")
    json_str = cfg_file.read()
    cfg_file.close()
    json = ujson.loads(json_str)
    
    return json
