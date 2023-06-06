#!/bin/bash

subject="System Rebooted"
recipient="rasmc19@student.sdu.dk"
message="The system has needed to reboot."

echo "$message" | mail -s "$subject" "$recipient"
