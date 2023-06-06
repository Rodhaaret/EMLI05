#!/bin/bash

# Get the current date and time
current_datetime=$(date +"%Y-%m-%d %H:%M:%S")

while read -r line </dev/ttyACM0; do
    values=$(echo "$line" | awk '{ for(i=1;i<=NF;i++) printf "%s ", $i }')
    values=${values//[\(\),]/}

    # Separate the values into an array
    IFS=' ' read -ra value_array <<< "$values"
    Plant=${value_array[0]}
    Pump=${value_array[1]}
    Moist=${value_array[2]}
    Light=${value_array[3]}

    # Maximum number of entries to keep
    MAX_ENTRIES=100

    # Check if text files exist
    if [[ ! -f "/home/pi/PlantAlarm.txt" ]]; then
        touch "/home/pi/PlantAlarm.txt"
    fi
    if [[ ! -f "/home/pi/PumpAlarm.txt" ]]; then
        touch "/home/pi/PumpAlarm.txt"
    fi
    if [[ ! -f "/home/pi/MoistSensor.txt" ]]; then
        touch "/home/pi/MoistSensor.txt"
    fi
    if [[ ! -f "/home/pi/LightSensor.txt" ]]; then
        touch "/home/pi/LightSensor.txt"
    fi

    # Append new values to text files
    echo "Date & Time: $current_datetime | ${Plant}" >> "/home/pi/PlantAlarm.txt"
    echo "Date & Time: $current_datetime | ${Pump}"  >> "/home/pi/PumpAlarm.txt"
    echo "Date & Time: $current_datetime | ${Moist}" >> "/home/pi/MoistSensor.txt"
    echo "Date & Time: $current_datetime | ${Light}" >> "/home/pi/LightSensor.txt"

    # Remove the oldest entry 
    if [[ $(wc -l < "/home/pi/PlantAlarm.txt") -gt $MAX_ENTRIES ]]; then
        sed -i '1d' "/home/pi/PlantAlarm.txt"
        sed -i '1d' "/home/pi/PumpAlarm.txt"
        sed -i '1d' "/home/pi/MoistSensor.txt"
        sed -i '1d' "/home/pi/LightSensor.txt"
    fi
    break
done
