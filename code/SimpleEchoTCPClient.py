# # # # # # # # # # # # #
# BasicEchoTCPClient.py #
# 20124602 Lee Sueng Jun#
# # # # # # # # # # # # #

from socket import *

serverName = '192.168.56.1'
# serverName = 'nsl2.cau.ac.kr'
serverPort = 24602

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

print("The client is running on port", clientSocket.getsockname()[1])

message = input('Input lowercase sentence: ')

clientSocket.send(message.encode())

modifiedMessage = clientSocket.recv(2048)
print('Reply from server:', modifiedMessage.decode())

clientSocket.close()
