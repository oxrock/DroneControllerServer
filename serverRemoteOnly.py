import socket
from threading import Thread


appCommands = ['forward','backward','left','right','action 1','action 2','action 3','action 4','stop']

def main():
    global remoteProcess
    
    remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    remoteThread = Thread(target=remoteListener, args = (remoteSocket,))
    remoteThread.setDaemon(True)
    remoteThread.start()
    
    response = ""
    while response != "quit":
        response = raw_input("Enter 'quit' to exit the program.\n").lower()
        
    print("Exiting program")
      
    
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
    
   
        
def moveForward():
    print("replace me with relevant drone code!")
    

if __name__ == "__main__":
    main()
