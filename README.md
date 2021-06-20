# Sens MQTT node

## Summary

Micropython script for publishing humidity and temperature data to MQTT broker.
Tested on ESP8266 and ESP32 microcontrollers.

## Setup and flashing

Clone repository and submodules:
```
git clone --recursive github.com:spasoye/home_assistant_esp8266_node.git
```
Now you can start modifyng and/or flash code to board.
Currently I'm using [Thonny][Thonny] IDE for development of *upython* 
applications. Thonny offers scarce editor but its equiped with tools for 
access boards file system and makes developing easier.

After installing and running *Thonny*:
  * Select repository path in *Files* side menu under *This computer*
  * Setup the path to your board serial port. In toolbar *Run>Seletc interpreter*, selectyour board andpath to its serial port.

Modify *config.json* according to your setup. Select *boot.py*, *config.json* and *main.py* right click and *Upload to /*.



## TODO

[Thonny]: https://thonny.org/