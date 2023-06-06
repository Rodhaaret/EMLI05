#!/bin/bash

# Send email of reboot
./mailsend.sh

# Disable I/O & connections
./disable_USB.sh
./disable_Bluetooth.sh

# Set up Access Point Connection
sudo nmcli con up emli_05

# Set Pi dialout
sudo chmod 666 /dev/ttyACM0

# Open Foxglove Studio
#foxglove localhost:8765

# Start the system
. install/setup.bash

ros2 launch plantsystem launch_plantsystem.py



