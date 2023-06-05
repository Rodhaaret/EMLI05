# #!/bin/sh
while read -r line </dev/ttyACM0; do
    values=$(echo "$line" | grep -oP '\d+(?:\.\d+)?')
    echo $values
    break
done