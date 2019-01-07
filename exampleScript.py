#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 12:23:34 2018

The following code is what I use to control my own pi ground drone. If you are not using an adafruit motorhat, much of it will not be 
directly applicable to your own project. It should however give you a good idea of how to create your own functions to handle transmissions
from the remote drone controller app to control your creation.

This script is compatible with versions 1.2+

@author: oxrock
"""

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import socket
import RPi.GPIO as GPIO
import cv2
from threading import Thread

lights = False


commands = ['forward','reverse','left','right','action 1','action 2','action 3','action 4','stop']
moveSpeed = 300

mh = Adafruit_MotorHAT(addr=0x60)
motors = [mh.getMotor(1),mh.getMotor(2),mh.getMotor(3),mh.getMotor(4)]
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
ledPin1 = 36
ledPin2 = 32
GPIO.setup(ledPin1, GPIO.OUT)
GPIO.setup(ledPin2, GPIO.OUT)


def toggleLights():
	global lights
	lights = not lights
	if lights:
		GPIO.output(ledPin1, GPIO.HIGH)
		GPIO.output(ledPin2, GPIO.HIGH)
	else:
		GPIO.output(ledPin1, GPIO.LOW)
		GPIO.output(ledPin2, GPIO.LOW)
        

def turnRight():
	motors[0].run(Adafruit_MotorHAT.FORWARD)
	motors[0].setSpeed(moveSpeed)
	motors[1].run(Adafruit_MotorHAT.FORWARD)
	motors[1].setSpeed(moveSpeed)
	motors[2].run(Adafruit_MotorHAT.BACKWARD)
	motors[2].setSpeed(moveSpeed)
	motors[3].run(Adafruit_MotorHAT.BACKWARD)
	motors[3].setSpeed(moveSpeed)

def turnLeft():
	motors[2].run(Adafruit_MotorHAT.FORWARD)
	motors[2].setSpeed(moveSpeed)
	motors[3].run(Adafruit_MotorHAT.FORWARD)
	motors[3].setSpeed(moveSpeed)
	motors[0].run(Adafruit_MotorHAT.BACKWARD)
	motors[0].setSpeed(moveSpeed)
	motors[1].run(Adafruit_MotorHAT.BACKWARD)
	motors[1].setSpeed(moveSpeed)

def moveForward():
	motors[0].run(Adafruit_MotorHAT.FORWARD)
	motors[0].setSpeed(moveSpeed)
	motors[1].run(Adafruit_MotorHAT.FORWARD)
	motors[1].setSpeed(moveSpeed)
	motors[2].run(Adafruit_MotorHAT.FORWARD)
	motors[2].setSpeed(moveSpeed)
	motors[3].run(Adafruit_MotorHAT.FORWARD)
	motors[3].setSpeed(moveSpeed)

def moveBackward():
	motors[0].run(Adafruit_MotorHAT.BACKWARD)
	motors[0].setSpeed(moveSpeed)
	motors[1].run(Adafruit_MotorHAT.BACKWARD)
	motors[1].setSpeed(moveSpeed)
	motors[2].run(Adafruit_MotorHAT.BACKWARD)
	motors[2].setSpeed(moveSpeed)
	motors[3].run(Adafruit_MotorHAT.BACKWARD)
	motors[3].setSpeed(moveSpeed)

def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

      



def main():
    global remoteProcess
    global videoProcess
    
    remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    camSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    remoteThread = Thread(target=remoteListener, args = (remoteSocket,))
    remoteThread.setDaemon(True)
    remoteThread.start()
    
    camThread = Thread(target=imageStreamer, args = (camSocket,))
    camThread.setDaemon(True)
    camThread.start()
    
    response = ""
    while response != "quit":
        response = raw_input("Enter 'quit' to exit the program.\n").lower()
        
    print("Exiting program")
    
    
def structureByteHeader(numberBytes,desiredLength):
    #sets the byte header to a uniform length that the app expects while allowing custom resolutions
    while len(numberBytes) < desiredLength:
        numberBytes +=  str(" ").encode()
    return numberBytes
    
def remoteListener(socket):
    socket.bind(("", 8085)) #80815 is the port this socket will be listening for, this number has to match the remote port assigned in the app.
    socket.listen(1) #set how many connections to accept
    remoteConnection,address = socket.accept()

    while True:
        try:
            buf = remoteConnection.recv(1024)
            buf = buf.decode("utf-8")
            print(buf) 
            if len(buf) > 0:
                if buf == commands[0]:
                    moveForward()
                elif buf == commands[1]:
                    moveBackward()
                elif buf == commands[2]:
                    turnLeft()
                elif buf == commands[3]:
                    turnRight()
                elif buf == commands[4]:
                		toggleLights()
                elif buf == commands[8]:
                		turnOffMotors()
                    
            else:
                remoteConnection,address = socket.accept()
        except Exception as e:
            print(e)
            break
    
    

def imageStreamer(socket):
    cam = cv2.VideoCapture(0)
    socket.bind(("",8081)) # 8081 is the port this socket will be listening for, this number has to match the video port assigned in the app.
    socket.listen(1)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)#modify to set camera resolution width
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)#modify to set camera resolution height

    imageQuality = 50 #1-100 higher = better quality but more data
   
    # set flip image to True if you want the image to be flipped
    flipImage = False
    
    while True:
        try:
            client,address = socket.accept()
            ret,camImage = cam.read()
            if flipImage:
                camImage = cv2.flip(camImage,1)
            
            # reduce size of image for potentially faster streaming. Keep the 'fx' and 'fy' values the same or the image will become skewed.
            camImage = cv2.resize(camImage, (0,0), fx=0.5, fy=0.5)
            
            byteString = bytes(cv2.imencode('.jpg', camImage,[int(cv2.IMWRITE_JPEG_QUALITY), imageQuality])[1].tostring())
            fileSize = len(byteString)
            totalSent = 0
	    byteString = structureByteHeader(str(fileSize).encode(),8)+byteString
            
            totalSent = 0
            while totalSent < fileSize:
                totalSent += client.send(byteString[totalSent:])
           
        
        except Exception as e:
            print(e)
            break
        
    
if __name__ == "__main__":
    main()



