# # # # # # # # # # # # #
# BasicEchoTCPServer.py #
# 20124602 Lee Sueng Jun#
# # # # # # # # # # # # #

from socket import *
from signal import *
import datetime

def toUpper():
    client_message = connectionSocket.recv(2048)
    capitalized_message = client_message.decode().upper()
    connectionSocket.send(capitalized_message.encode())

def SendIP_Port():
    client_IP, client_port = clientAddress
    client_data = "IP={}\t port= {}".format(client_IP,client_port)
    connectionSocket.sendall(client_data.encode())

serverPort = 24602 # 34602,44602,54602
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("The server is ready to receive on port", serverPort)
(connectionSocket, clientAddress) = serverSocket.accept()

request_number = 0
while True:
    print('Connection requested from', clientAddress)
    message = connectionSocket.recv(2048)
    selection = message.decode()
    request_number += 1
    request_number += 1  # increment of number when server recieves request from client

    if selection == "1":  # capitalization
        print("Requested Command 1 by", self.name)
        client_message = self.socket.recv(2048)
        capitalized_message = client_message.decode().upper()
        self.socket.send(capitalized_message.encode())

    elif selection == "2":  # get my ip addr. and port number
        print("Requested Command 2 by", self.name)
        self.address, self.port = clientAddress
        client_data = "IP={}\t port= {}".format(self.address, self.port)
        self.socket.sendall(client_data.encode())  # sends encoded message with multiple datas to client

    elif selection == "3":  # get server's local datetime
        print("Requested Command 3 by", self.name)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # save datetime info. without milli-second
        self.socket.send(bytes(str(now).encode()))  # (int -> string) into bytes for encoding

    elif selection == "4":  # get my total requested number
        print("Requested Command 4 by", self.name)
        self.socket.send(bytes(str(request_number).encode()))

    elif selection == "5":  # exit by entering number 5
        ClientHandler.count -= 1
        print("Client", self.name, "Disconnected. Number of connected clients : ", ClientHandler.count)
        break

    elif selection == "":  # keyboard interruption message from client decoded as null string
        ClientHandler.count -= 1
        print("Client", self.name, "Disconnected. Number of connected clients : ", ClientHandler.count)
        break

    else:  # recieved invalid function
        print("Invalid Function requested")

connectionSocket.close()
serverSocket.close()