#!/bin/bash

# Email configuration
recipient="rasmc19@student.sdu.dk"
subject="System Rebooted"
body="The system has rebooted"

# Send email of reboot
echo "$body" | mail -s "$subject" "$recipient"

#sudo sysctl -w net.ipv4.ip_forward=1                        # Måske skal det fjernes
#sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE   # Måske skal det fjernes

# Set up Access Point Connection
sudo nmcli con up emli_05

# Set Pi dialout
sudo adduser pi dialout

# Set Pi dialout
sudo chmod 666 /dev/ttyACM0