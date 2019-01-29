# DroneControllerServer
An example server script to use in conjunction with "Drone Controller With Video" app on google playstore: https://play.google.com/store/apps/details?id=com.oxrockstudio.DroneRemoteControllerWithVideo

The provided sample code should work for either python 2 or 3, although it was tested mainly on 2.7. If you're using this code on a raspberry pi, then I suggest trying to get it working on python 2 if possible. This script requires opencv which can be a larger hassle to install properly for python 3 on raspberry pi devices.

In an effort to improve accessibility as well as performance, you  now have the option to view MJPEG streams such as those used in the popular pi program Motion. Users controlling drones across vast distances should see an INCREDIBLE improvements to video response times if utilizing the new motion functionality.

Motion is really easy to setup especially with the help of a guide like this one: https://pimylifeup.com/raspberry-pi-webcam-server/

A server script will still need to run on your pi device to to handle drone inputs. if you're using motion for streaming video, you'll need to trim out the existing camera code. Using Motion is by no means mandatory. If your script worked in version 1.2, it will still work in version 1.25. Just make sure "Server Script" is selected from the drop down menu in video options.

Installing opencv for python2 on pi should be simply accomplished by the following(If not using motion to handle video streaming):

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

