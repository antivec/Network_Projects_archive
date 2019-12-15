# # # # # # # # # # # #  #
# MultiThreadTCPServer.py#
# 20124602 Lee Sueng Jun #
# # # # # # # # # # # #  #

from socket import *
from threading import Lock,Thread,Timer
from signal import *
import time
import datetime
import torch.nn

# function for when (Ctrl+C) detected, exit gracefully
def signal_handling(signum,frame):
    print("CTRL+C detected \n Bye Bye!!")
    try:
        connectionSocket.close()
        serverSocket.close()
        print("Sockets are now closed")
    except NameError:
        print("No Connection has been made")
    exit(0)

# Class of Multi-thread connection
class ClientHandler(Thread):
    count = 0
    def __init__(self, name, address, port, socket, lock): # initialize values for each registered clients
        Thread.__init__(self)
        self.name = name
        self.address = address
        self.port = port
        self.socket = socket
        self.lock = lock
        ClientHandler.count += 1 # total number of clients connected to the server

    # Define the actions the thread will execute when called.
    def run(self):
        request_number = 0
        print("Client", self.name, " Connected. Number of connected clients : ", ClientHandler.count)
        while True:
            message = ""
            message = self.socket.recv(2048)
            selection = message.decode() # decodes message from client
            request_number += 1 # increment of number when server recieves requestment from client

            if selection == "1":
                print("Requested Command 1 by", self.name)
                client_message = self.socket.recv(2048)
                capitalized_message = client_message.decode().upper()
                self.socket.send(capitalized_message.encode())
            elif selection == "2":
                print("Requested Command 2 by", self.name)
                self.address, self.port = clientAddress
                client_data = "IP={}\t port= {}".format(self.address, self.port)
                self.socket.sendall(client_data.encode())  # sends encoded message with multiple datas to client
            elif selection == "3":
                print("Requested Command 3 by", self.name)
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # save datetime info. without milisecond
                self.socket.send(bytes(str(now).encode()))  # (int -> string) into bytes for encoding
            elif selection == "4":
                print("Requested Command 4 by", self.name)
                self.socket.send(bytes(str(request_number).encode()))
            elif selection == "5":
                ClientHandler.count -= 1
                print("Client", self.name, "Disconnected. Number of connected clients : ", ClientHandler.count)
                break
            elif selection == "": # keyboard interruption message from client decoded as null string
                ClientHandler.count -= 1
                print("Client", self.name, "Disconnected. Number of connected clients : ", ClientHandler.count)
                break
            else: # recieved invalid function
                print("Invalid Function requested")


def Print_Num_of_Client(): # fuction for printing number of clients
    print("Number of connected clients :", ClientHandler.count)
    Timer(60.0, Print_Num_of_Client).start() # restart the timer



# Main
signal(SIGINT,signal_handling) # ctrl+c detection
threads = []            # activated thread list
thread_lock = Lock()

client_name = 0

serverPort = 24602  # 34602,44602,54602
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
serverSocket.bind(('', serverPort))

print("The server is ready to receive on port", serverPort)
print("Press(Ctrl+C) to close the server")
Timer(60.0, Print_Num_of_Client).start()  # repeats number of client per 60 seconds

while True:
    serverSocket.listen(1)
    (connectionSocket, clientAddress) = serverSocket.accept()
    client_name += 1 #assigning number for client
    newThread = ClientHandler(client_name,clientAddress[0], clientAddress[1], connectionSocket, thread_lock)
    threads.append(newThread)
    newThread.start()


connectionSocket.close()
serverSocket.close()
print("Close called")