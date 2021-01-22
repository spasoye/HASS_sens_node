from umqtt.simple import MQTTClient
import machine
import dht
import utime
import ntptime
import ujson
import time
from machine import Timer
from machine import Pin

relay_pin = None
sensor = None
client = None
node_name = None

def mqtt_init():
    global client
    print("Initializing MQTT client.")
    print("node name:", node_name)
    client = MQTTClient(node_name, broker)
    client.set_callback(mqtt_msg)

    client.connect()
  
def mqtt_msg(topic, msg):
    print("topic:", topic)
    print("message:", msg.decode("utf-8"))
    
    if topic.decode("utf-8") == (node_name + "/relay/set"):
        if msg.decode("utf-8") == 'OFF':
            print("LED OFF")
            client.publish(node_name + "/relay", "OFF")
            relay_pin.value(1)
        if msg.decode("utf-8") == 'ON':
            print("LED ON")
            client.publish(node_name + "/relay", "ON")
            relay_pin.value(0)

def wifi_connect(ssid, password):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network: ', ssid )
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def sensor_read(timer):
    global sensor
    global client
    
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    
    time = utime.localtime()
    
    print("sensor read")
    
    try:
        client.publish(node_name + "/status", "online")
        client.publish(node_name + "/sens", "{ \"temp\": " + str(temp) +", \"hum\": " + str(hum) + "}")
    except Exception as e:
        print("fail while publishing:", e)
        machine.reset()
    
# read this from file
cfg_file = open("config.json", "r")
json_str = cfg_file.read()
cfg_file.close()
json = ujson.loads(json_str)

node_name = json["name"]
ssid = json["ssid"]
password = json["pass"]
broker = json["broker"]
dht_pin = json["dht_pin"]
relay_pin = json["relay_pin"]
period = int(json["period"])

relay_pin = Pin(dht_pin, Pin.OUT)

print("starting the sensor")
# connect to network
wifi_connect(ssid, password)

# Initialize DHT sensor
print("Initializing DHT sensor.")
sensor = dht.DHT22(machine.Pin(dht_pin))

tim = Timer(4)
tim.init(mode=Timer.PERIODIC, period=period*1000, callback=sensor_read)

# Initialize MQTT client and subscribe to rx_topic
mqtt_init()
while True:
    try:
        client.subscribe(node_name + '/relay/set')
        client.subscribe(node_name + '/available')
        client.subscribe(node_name + '/attributes')
    except Exception as e:
        # Need to handle different errors differently
        print("desilo se:",e)
        machine.reset()
        pass
    
    

