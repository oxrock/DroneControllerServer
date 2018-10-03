#!/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 13:30:45 2018

@author: oxrock
"""


import cv2
import socket
from threading import Thread


def main():
    global remoteProcess
    global videoProcess
    
    remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    camSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    remoteThread = Thread(target=remoteListener, args = (remoteSocket,))
    remoteThread.start()
    
    camThread = Thread(target=imageStreamer, args = (camSocket,))
    camThread.start()
    
    response = ""
    while response != "quit":
        response = input("Enter 'quit' to exit the program.\n").lower()
        
    print("Exiting program")
    
    # closing the below sockets will cause errors in their threads. This is required to break out of their respective while loops and terminate properly.
    
    remoteSocket.close()
    camSocket.close()
    
    
    
def remoteListener(socket):
    socket.bind(("", 8085)) #80815 is the port this socket will be listening for, this number has to match the remote port assigned in the app.
    socket.listen(1) #set how many connections to accept
    remoteConnection,address = socket.accept()

    while True:
        try:
            buf = remoteConnection.recv(1024)
            buf = buf.decode("utf-8") 
            if len(buf) > 0:
                print(buf)
                #use 'buf' to to call functions or perform actions based on it's value, EXAMPLE:
                if buf == "forward":
                    moveForward()
                elif buf == 'disconnect':
                    print("app is attempting to disconnect")#you could use this for your own terminate function here or just ignore
                    
            else:
                remoteConnection,address = socket.accept()
        except Exception as e:
            #print(e)
            break
    
    

def imageStreamer(socket):
    cam = cv2.VideoCapture(0)
    socket.bind(("",8081)) # 8081 is the port this socket will be listening for, this number has to match the video port assigned in the app.
    socket.listen(1)
    
    #cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #uncomment and modify to set camera resolution width
    #cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) #uncomment and modify to set camera resolution height
   
    # set flip image to False if you don't want the image to be flipped
    flipImage = True
    
    while True:
        try:
            client,address = socket.accept()
            ret,camImage = cam.read()
            if flipImage:
                camImage = cv2.flip(camImage,1)
            
            # reduce size of image for potentially faster streaming. Keep the 'fx' and 'fy' values the same or the image will become skewed.
            camImage = cv2.resize(camImage, (0,0), fx=0.5, fy=0.5)
            
                
            #Remove both sets of ''' to uncomment the below code and view the webcam stream on this device. Mostly useful for testing purposes
            '''
            cv2.imshow('image',camImage)
            if cv2.waitKey(1) == 27: 
                break  # esc to quit
            ''' 
            byteString = bytes(cv2.imencode('.jpg', camImage)[1].tostring())
            fileSize = len(byteString)
            totalSent = 0
            client.send(str(fileSize).encode())
            
            sizeConfirmation = client.recv(1024)
            
            totalSent = 0
            while totalSent < fileSize:
                totalSent += client.send(byteString[totalSent:])
              
            # this print statemen will give you a readout of the image's byte size, the amount of bytes sent over the connection, and the count of bytes recieved at the destination
            #print(str(fileSize), str(totalSent),sizeConfirmation.decode('utf-8'))
        
        except Exception as e:
            #print(e)
            break
        
def moveForward():
    print("replace me with relevant drone code!")
    


    
    
if __name__ == "__main__":
    main()
