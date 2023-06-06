#!/bin/bash

# Check if Bluetooth is already blocked
if rfkill list bluetooth | grep -q "Soft blocked: yes"; then
    echo "Bluetooth is already disabled."
else
    # Block Bluetooth
    rfkill block bluetooth
    echo "Bluetooth disabled."
fi
