from umqtt.simple import MQTTClient
import machine
import bme280
import utime
import ntptime
import ujson
import time
from machine import Timer
from machine import Pin
import sys

relay = None
sensor = None
client = None
node_name = None

def sensor_init():
    global sensor
    
    print("Initializing sensor.")

    pinSDA = machine.Pin(sda_pin)
    pinSCL = machine.Pin(scl_pin)

    i2c = machine.I2C(scl=pinSCL, sda=pinSDA)

    sensor = bme280.BME280(i2c=i2c)

def sensor_read(timer):
    global sensor
    global client
    
    #sensor.measure()
    temp,press,hum = sensor.read_compensated_data()

    # C
    temp = temp / 100
    # hPa
    press = press / 256
    press = press / 100
    # %
    hum = hum / 1024
    
    time = utime.localtime()
    
    print("sensor read:", temp,press,hum)
    
    try:
        client.publish("node1/status", "online")
        client.publish(node_name + "/sens", "{ \"temp\": " + str(temp) +", \"hum\": " + str(hum) +", \"press\": " + str(press) + "}")
    except Exception as e:
        print("fail while publishing:", e)
        machine.reset()

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
    
# read this from file
cfg_file = open("config.json", "r")
json_str = cfg_file.read()
cfg_file.close()
json = ujson.loads(json_str)

node_name = json["name"]
ssid = json["ssid"]
password = json["pass"]
broker = json["broker"]
sda_pin = json["sda_pin"]
scl_pin = json["scl_pin"]
period = int(json["period"])

print("starting the sensor")
# connect to network
wifi_connect(ssid, password)

# Initialize DHT sensor
sensor_init()

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
        sys.exit()
        pass
    
#TODO:
    
#import machine
#>>> pinSDA = machine.Pin(5)
#>>> pinSDA
#Pin(5)
#>>> pinSDA = machine.Pin(4)
#>>> pinSCL = machine.Pin(5)
#>>> bus = I2C(scl=pinSCL, sda=pinSDA)
#>>> bmp = BMP280(bus)
#https://github.com/dafvid/micropython-bmp280

