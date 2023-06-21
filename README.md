# BotC Lights #

BotC Lights allows you to represent the townsquare of [Blood on the Clocktower](https://bloodontheclocktower.com) as a strip of lights controlled by your phone over bluetooth. Each light representing a player and whether they are alive, dead with a vote or dead without a vote.

# Prerequisites  #

## You will need ##

1. [Pimoroni Plasma Stick 2040 W](https://shop.pimoroni.com/products/plasma-stick-2040-w?variant=40359072301139) / [Pimoroni Plasma Stick 2040 W Kit](https://shop.pimoroni.com/products/wireless-plasma-kit?variant=40372594704467)

2. NeoPixel/WS2812 compatible lights [like these](https://shop.pimoroni.com/products/5m-flexible-rgb-led-wire-50-rgb-leds-aka-neopixel-ws2812-sk6812?variant=40384556171347)

3. Small flathead screwdriver

4. A way to connect the Plasma Stick to your computer (USB micro-B)

5. A way to power the Plasma Stick (USB micro-B)

## Assembling Plasma Stick ##

[Assembling Wireless Plasma Kit](https://learn.pimoroni.com/article/assembling-wireless-plasma-kit)

## Update Plasma Stick Firmware ##

https://learn.pimoroni.com/article/getting-started-with-pico#installing-the-custom-firmware

You will want firmware `pimoroni-picow-v1.20.3-micropython.uf2` or later

## Install Python ##
https://python.land/installing-python

# Install Code #

1. Install mpremote
```console
$ pip install mpremote
```

2. Find device id
```console
$ mpremote devs
/dev/cu.usbmodem101 e6614c311b893a25 2e8a:0005 MicroPython Board in FS mod
```
The device id would be `e6614c311b893a25` in this example

3. Install the code onto the Plasma Stick 2040 W
```console
$ mpremote connect id:e6614c311b893a25 mip install github:North101/botc_lights

$ mpremote connect id:e6614c311b893a25 mip install --target ./ github:North101/botc_lights/main.py
```

# Install App #

## Android ##

Join testing: https://play.google.com/apps/internaltest/4701706597907158436

## iOS ##

Not available yet

# Running #

When the Plasma Stick 2040 W is powered, it should automatically run the code. If everything is working correctly you will see the LED on it start flashing green.

Next open up the app on your phone. You will need to allow bluetooth permissions and then it will start scanning for the plasma stick over bluetooth.

When a button called "BotC Lights" appears on screen that means your phone has found it!
