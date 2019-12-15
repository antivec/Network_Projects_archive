# # # # # # # # # # # # #
# BasicEchoTCPServer.py #
# 20124602 Lee Sueng Jun#
# # # # # # # # # # # # #

from socket import *
import datetime

def toUpper(): # Function for Capitalization
    client_message = connectionSocket.recv(2048)
    capitalized_message = client_message.decode().upper()
    connectionSocket.send(capitalized_message.encode())

def SendIP_Port(): # returns client's IP and port information
    client_IP, client_port = clientAddress
    client_data = "IP={}\t port= {}".format(client_IP,client_port)
    connectionSocket.sendall(client_data.encode()) # sends encoded message with multiple datas to client

def SendLocalServerTime(): # returns local time (Server's) to client
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # save datetime info. without milisecond
    connectionSocket.send(bytes(str(now).encode())) # (int -> string) into bytes for encoding

def SendTotalRequested(): # returns total number of requested message from client
    connectionSocket.send(bytes(str(request_number).encode()))

terminate = False # keyboardInterrupt flag

def signal_handling(signum,frame):# used for detecting keyboardInterrupt(ctrl+C)
	global terminate				  # once it detects keyboard interruption
	terminate = True				  # flag 'terminate' becomes true

serverPort = 24602 # 34602,44602,54602
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to receive on port", serverPort)

(connectionSocket, clientAddress) = serverSocket.accept()
print("The server is now connected to ", clientAddress)
#connectionSocket.settimeout(5)
# serverSocket.connect(clientAddress)

request_number = 0
while True:
    # try:
    message = connectionSocket.recv(2048)
    selection = message.decode() # decodes message from client
    request_number += 1 # increment of number when server recieves requestment from client
    # except connectionSocket.timeout:
    #     connectionSocket.close()
    #     serverSocket.close()
    #     print("Timeout Occured \n")
    #     print("Bye Bye")
    #     exit(0)

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
        print("Termination requested from Client")
        break
    elif selection == "": # keyboard interruption message from client decoded as null string
        print("Termination requested from Client")
        break
    else: # recieved invalid function
        print("Invalid Function requested")

    if terminate:  # ctrl+c shutdown with closing client socket
        connectionSocket.close()
        serverSocket.close()
        print("Ctrl+C interruption detected \n")
        print("Bye Bye")
        exit(0)


#Connection ended, closing sockets
connectionSocket.close()
serverSocket.close()