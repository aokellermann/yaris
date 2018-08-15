#### Interface for backup cam and radar for Linux.

### Setup
Install all dependencies:
* python2
* python2-pyserial
* alsa-utils
* mplayer

The program will use /dev/video0 for the camera and /dev/ttyUSB0 for the radar serial data. I'm using a webcam for the camera and a MakerFocus Lidar Range Finder Sensor Module ($40 off amazon) connected to a TTL to USB adapter for the radar. By default, /dev/ttyUSB0 will be owned by root, which can be changed with a udev rule.
``` bash
echo "SUBSYSTEM==\"tty\", KERNEL==\"ttyUSB0\", GROUP=\"dialout\", MODE=\"0660\"" | sudo tee /etc/udev/rules.d/99-ttyusb.rules
sudo groupadd dialout
sudo usermod -a -G dialout $USER 
```
Reboot after running these commands

After logging back in, you can install by running
``` bash
git clone https://github.com/aokellermann/yaris.git && cd yaris
sudo make install
```
