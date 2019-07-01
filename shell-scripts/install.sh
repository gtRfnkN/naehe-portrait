#!/bin/bash
clear
echo "=== Starting installation of Family Portrait ==="

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as sudo!" 1>&2
   exit 1
fi

echo " -- START: Installing software using apt-get --"
apt-get update && apt-get upgrade
apt-get install -y git python python-rpi.gpio python-dev python-pip fswebcam
pip install evdev
echo " -- DONE:  Installing software using apt-get --"


echo " -- START: Downloading chromium-browser --"
wget http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-browser-l10n_48.0.2564.82-0ubuntu0.15.04.1.1193_all.deb
wget http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-browser_48.0.2564.82-0ubuntu0.15.04.1.1193_armhf.deb
wget http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-codecs-ffmpeg-extra_48.0.2564.82-0ubuntu0.15.04.1.1193_armhf.deb
echo " -- DONE:  Downloading chromium-browser --"

echo " -- START: Installing chromium-browser --"
dpkg -i chromium-codecs-ffmpeg-extra_48.0.2564.82-0ubuntu0.15.04.1.1193_armhf.deb
dpkg -i chromium-browser-l10n_48.0.2564.82-0ubuntu0.15.04.1.1193_all.deb chromium-browser_48.0.2564.82-0ubuntu0.15.04.1.1193_armhf.deb
echo " -- DONE:  Installing chromium-browser --"


echo " -- START: Adding naehe-portrait service --"
chmod +x /home/pi/naehe-portrait/main.py
cp /home/pi/naehe-portrait/shell-scripts/naehe-portrait-service /etc/init.d/
chmod +x /etc/init.d/naehe-portrait-service
update-rc.d naehe-portrait-service defaults
echo " -- DONE:  Adding naehe-portrait service --"


echo " -- START: Removing screensaver --"
cp /etc/xdg/lxsession/LXDE-pi/autostart /etc/xdg/lxsession/LXDE-pi/autostart.bak
cp /etc/xdg/lxsession/LXDE/autostart /etc/xdg/lxsession/LXDE/autostart.bak
cp /home/pi/naehe-portrait/shell-scripts/autostart-pi.txt /etc/xdg/lxsession/LXDE-pi/autostart
cp /home/pi/naehe-portrait/shell-scripts/autostart.txt /etc/xdg/lxsession/LXDE/autostart
echo " -- DONE:  Removing screensaver --"


echo " -- START: Adding autostart naehe-portrait website --"
mkdir /home/pi/.config/autostart/
cp /home/pi/naehe-portrait/shell-scripts/autoChromium.desktop /home/pi/.config/autostart/autoChromium.desktop
echo " -- DONE:  Adding autostart naehe-portrait website --"


echo "=== Finished installation of Family Portrait ==="

echo ">>> Rebooting in 5 seconds <<<"
sleep 1
echo ">>> Rebooting in 4 seconds <<<"
sleep 1
echo ">>> Rebooting in 3 seconds <<<"
sleep 1
echo ">>> Rebooting in 2 seconds <<<"
sleep 1
echo ">>> Rebooting in 1 seconds <<<"
sleep 1
echo ">>>  Rebooting right now   <<<"
reboot