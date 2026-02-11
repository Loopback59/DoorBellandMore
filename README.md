Sends MQTT stuff to Shelly relays for On and Off of lights etc.
Raspberry pi 3 with small touchscreen

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
pip install paho-mqtt

Backlight is controlled by sensor connected to a GPIO
Executes for ON
echo "1" | sudo tee /sys/class/backlight/soc\:backlight/brightness
or for OFF
echo "0" | sudo tee /sys/class/backlight/soc\:backlight/brightness

Add route somewhere
sudo ip route add 192.168.50.0/24 via 192.168.1.155 dev enp3s0

