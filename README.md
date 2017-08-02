# DCZia BLE Scanner (Defcon 2017)

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

## Screenshots
![screen capture](http://i.imgur.com/Sbw7CCq.png)

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
