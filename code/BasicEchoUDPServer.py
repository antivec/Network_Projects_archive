# # # # # # # # # # # # #
# BasicEchoUDPServer.py #
# 20124602 Lee Sueng Jun#
# # # # # # # # # # # # #

from socket import *
import datetime


def toUpper(): # Function for Capitalization
    (request_capital, clientAddress) = serverSocket.recvfrom(2048)
    capitalized_message = request_capital.decode().upper()
    serverSocket.sendto(capitalized_message.encode(), clientAddress)

def SendIP_Port(): # returns client's IP and port information
    client_IP, client_port = clientAddress
    client_data = "IP={}\t port= {}".format(client_IP, client_port)
    serverSocket.sendto(client_data.encode(),clientAddress)

def SendLocalServerTime(): # returns local time (Server's) to client
    TimeMessage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # save datetime info. without milisecond
    serverSocket.sendto(bytes(str(TimeMessage).encode()), clientAddress) # (int -> string) into bytes for encoding

def SendTotalRequested(): # returns total number of requested message from client
    serverSocket.sendto(bytes(str(request_count).encode()), clientAddress)


serverPort = 24602

serverSocket = socket(AF_INET, SOCK_DGRAM) # UDP Connection
serverSocket.bind(('', serverPort))

print("The server is ready to receive on port", serverPort)

request_count = 0
while True:
    (message, clientAddress) = serverSocket.recvfrom(2048)
    selection = message.decode() # decodes message from client
    request_count += 1 # increment of number when server recieves requestment from client

    if selection == "1":
        print("Requested Command 1 ")
        toUpper()
    elif selection == "2":
        print("Requested Command 2")
        SendIP_Port()
    elif selection == "3":
        print("Requested Command 3")
        SendLocalServerTime()
    elif selection == "4":
        print("Requested Command 4")
        SendTotalRequested()
    elif selection == "5":
        print("Termination confirmed from Client")
    elif selection == "INT": # keyboard interruption message from client decoded as null string
        print("Termination confirmed from Client")
    else: # recieved invalid function
        print("Invalid Function requested")

#Connection ended, closing sockets
serverSocket.close()
