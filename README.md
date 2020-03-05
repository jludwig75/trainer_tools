Trainer Tools
===

This module provides support for reading input from trainer and exercise sensors
and using that input to control other devices such as fans and LED strips. This
module is intended to be run from a Raspberry Pi with a USB ANT+ adapter and its
GPIO pins connected to relays or other devices.

Currently the following ANT+ sensors are supported
- Heart Rate Monitor
- Power Meter
- Speed and Cadence Sensors

The following devices can be controlled by the module:
- Four speed (off, low, medium, high) relay controlled fan
- LED Strip

The goal of this module is to keep adding support for more sensors and devices
and to make it easy to create interactions between sensors and devices.

The current interactions are currently available:
- Fan speed controlled by heart rate monitor
- LED strip light color controlled by power meter with colors that match Zwift
    power range colors

Installation
===
These scripts are written to run on Raspbian on a Raspberry Pi.

Pre install. It might be a good idea to make sure your Raspbian instal is up-to-date:
- sudo apt update
- sudo apt upgrade
- sudo reboot

Install Steps
---
- connect to shell on Raspberry Pi
- sudo apt install -y git
- git clone https://github.com/jludwig75/trainer_tools.git
- cd trainer_tools
- sudo ./setup.py
- Edit settings.cfg to set the correct athlete settings
- Edit device_settings.cfg for the correct hardware settings
- sudo reboot

Wiring
===
![Wiring Diagram](/wiring_diagram1.jpg)

WARNING: Be very careful wiring the fan to the relay. It is high voltage. If you are not
sure how to wire it, don't do it. Find someone to help you do it. It may be a
good idea to rewire the fan with a cord with a ground wire in a grounded receptacle.
If you add a ground wire, just make sure it is fastened with electrical contact
to the metal chasis of the fan.

Additional Information
===

The following interactions are being worked on:
- Cadence to control a segment of an LED strip
- Heart rate to control a segment of an LED strip

This module will also include a web interface through which a user can set their
FTP, fan speed heart rate zones and cadence zones. This web interface might
provide a way to create additional custom interactions, but we will need more
help to be able to do this. For now the plan is to create a cherrypi web server
to edit settings, start and stop interaction scripts and shutdown/reboot the
raspberry pi. The front end will be HTML with JavaScript (jQuery). We are open
to other options if we can find contributors willing to work on the web server.

It would also be good to add device discovery to the module and web interface.
Currently the module will connect to the first ANT+ sensor of a given type. It
also only supports ANT+, though it would not be hard to add ANT support.

History
===
This project was started by Michal Kozma to control a variable speed fan by
heart rate and control an LED strip using power data from a power meter.
Jonathan Ludwig has taken over the software development to make refinements.
