#!/bin/bash

# Get current date and time
current_date=$(date +"%Y-%m-%d")
current_time=$(date +"%H:%M:%S")

# Get available disk space in percent
disk_space=$(df -h | awk '$NF == "/" {print $5}')

# Get available RAM in percent
ram_usage=$(free | awk '/Mem/ {printf("%.2f"), $3/$2 * 100}')

# Get current CPU load in percent
cpu_load=$(top -bn1 | awk '/%Cpu/ {print $2}')

# Get CPU temperature in degrees Celsius
cpu_temp=$(vcgencmd measure_temp | awk -F "=" '{print $2}' | awk -F "'" '{print $1}')

# Get bytes transferred for eth0 interface
eth0_bytes=$(cat /sys/class/net/eth0/statistics/rx_bytes)

# Get bytes transferred for wlan0 interface
wlan0_bytes=$(cat /sys/class/net/wlan0/statistics/rx_bytes)

# Print the results
echo "Date: $current_date  |  Time: $current_time  |  Available Disk Space: $disk_space  |  " >> /home/pi/emli5_ws/system_info/diskspace.txt
echo "Date: $current_date  |  Time: $current_time  |  Available RAM: $ram_usage%  |  " >> /home/pi/emli5_ws/system_info/RAM.txt
echo "Date: $current_date  |  Time: $current_time  |  CPU Load: $cpu_load%  |  " >> /home/pi/emli5_ws/system_info/CPU_load.txt
echo "Date: $current_date  |  Time: $current_time  |  CPU Temperature: $cpu_temp°C  |  " >> /home/pi/emli5_ws/system_info/CPU_temp.txt
echo "Date: $current_date  |  Time: $current_time  |  Bytes Transferred (eth0): $eth0_bytes  |  " >> /home/pi/emli5_ws/system_info/eth0_trans.txt
echo "Date: $current_date  |  Time: $current_time  |  Bytes Transferred (wlan0): $wlan0_bytes  |  " >> /home/pi/emli5_ws/system_info/wlan0_trans.txt
