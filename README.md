# DroneControllerServer
An example server script to use in conjunction with "Drone Controller With Video" app on google playstore: https://play.google.com/store/apps/details?id=com.oxrockstudio.DroneRemoteControllerWithVideo

The provided sample code should work for either python 2 or 3, although it was tested mainly on 2.7. If you're using this code on a raspberry pi, then I suggest trying to get it working on python 2 if possible. This script requires opencv which can be a larger hassle to install properly for python 3 on raspberry pi devices.

Installing opencv for python2 on pi should be simply accomplished by the following:

sudo apt-get install python-numpy

sudo apt-get install python-scipy

sudo apt-get install python-opencv


camServer_v1.2.py is for communicating with Drone Controller With Video versions 1.2 and above.

camServer_OLD.py is for communicating with Drone Controller With Video versions 1.15 and below.

It is highly reccomended that you disable wifi powersave mode if you're streaming wirelessly. You can do so with the following command: sudo iw wlan0 set power_save off

It can also be beneficial to update your pi with the following commands:

sudo apt-get update

sudo apt-get dist-upgrade

sudo rpi-update

