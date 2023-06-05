#!/bin/bash

# Get a list of all USB ports
usb_ports=$(lsusb | grep -oP '\d+(?=:)' | sort -u)

# Iterate over each USB port
for port in $usb_ports; do
    # Check if the port is in use
    if lsusb -s $port:1 >/dev/null 2>&1; then
        echo "USB Port $port is in use"
    else
        echo "Disabling USB Port $port"
        uhubctl -a off -p $port
    fi
done
