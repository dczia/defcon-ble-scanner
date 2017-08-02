# DCZia BLE Scanner (Defcon 2017)

## Understanding output
(Please take a quick look at screenshot below then continue reading).

This application will show all nearby devices broadcasting over Bluetooth Low Energy (BLE or BTLE). The [Appearance ID](https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.characteristic.gap.appearance.xml) of `0xDC19` was used by Defcon 25 attendees that wanted their devices to be found; this application only accepts broadcasts with the `0xDC19` Appearance ID. 

#### Screen output
The output shown on your screen has two sections separated by [BLE Manufacturer Name](https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.characteristic.manufacturer_name_string.xml). The green section shows members of your group (this is configured in the `US` variable of `scan.py`). The default value is `0x5050` which is manufacturer name for DC Zia at Defcon. The blue/cyan section is for all other manufacturer names at Defcon 25 and also shows the manufacturer name (e.g. `0x9e04`)

#### Logging output
Each data capture from the pollling sequences will be logged out. The output has a format like:

~~~
2017-07-29 11:58:09.921733
PWNDC801 9e04 -81dB
HACKED 9e04 -79dB
F|5HT4P3 9e04 -74dB
DCZBitrunnr 5050 -67dB
~~~

Obviously, first line of output is the date of the data capture. Following the date will be a line for each unique received broadcast. The nName of the device, manufacturer name, and signal strength (in decibels) will be logged out. 

## Screenshots
![screen capture](http://i.imgur.com/Sbw7CCq.png)

## Preqrequisites
- [Raspberry Pi](https://www.raspberrypi.org/products/)
- [PiTFT](https://www.adafruit.com/product/2298)
- [Adafruit's Pre-built RPi Image](https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi/easy-install)

## Setup
~~~
# git clone https://github.com/dczia/dc25-ble-scanner.git
# cd dc25-ble-scanner
# virtualenv v
# source v/bin/activate
# pip install -r requirements.txt
# sudo ./scan.py
~~~

## Known Issues

#### 1. `bluepy.btle.BTLEException: Failed to execute mgmt cmd 'le on'`

This except can mean a few different things:

##### Insufficient privleges
1. Run `scan.py` as root.
2. Use `setcap` to enable privilge without always using root user:
~~~
sudo setcap 'cap_net_raw,cap_net_admin+eip' v/lib/python2.7/site-packages/bluepy/bluepy-helper
~~~

##### No device present
1. Ensure your BLE device is plugged in. Confirm this by running the command
below. You should see at least one device in Devices list.

~~~
# hcitool devices
Devices:
	hci0	00:1A:7D:DA:71:10
~~~
