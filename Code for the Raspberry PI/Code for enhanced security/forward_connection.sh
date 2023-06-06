#!/sbin/nft

 -fdefine WAN0 = wlan0 f
f
lush rulesettable ip nat 

{chain prerouting {type nat hook prerouting priority 0; policy accept;}

{type nat hook postrouting priority 100; policy accept;oifname $WAN0 masquerade}}
