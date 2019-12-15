#
# SimpleEchoUDPClient.py
#

from socket import *
from signal import *
import time

terminate = False # keyboardInterrupt flag

def signal_handling(signum,frame):# used for detecting keyboardInterrupt(ctrl+C)
	global terminate				  # once it detects keyboard interruption  
	terminate = True				  # flag 'terminate' becomes true

#Server information for connection
serverName = 'nsl2.cau.ac.kr'
serverPort = 24602
serverInfo = (serverName, serverPort)

# Connection configuration
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(('',serverPort))
print("The client is running on port", clientSocket.getsockname()[1])
signal(SIGINT,signal_handling)

# Succeed with connection to server
# loops until it gets exit command
while(True):
	start_time = 0 # initialize a variable for time
	print("<MENU>")
	print("1) Convert text to UPPER-case\n2) get my IP address and port number\n3) get Server time\n4) get server service count\n5) exit (or crtl+c)")
	message = input('\nInput function number: ')
	clientSocket.sendto(message.encode(),serverInfo)
	start_time = time.time()	# saves the time when user sends a command message

	if message == "1": # Convert to Upper-case
		print("==TEXT TO UPPER-CASE==\n")
		request_capital = input("Input Message: ")

		clientSocket.sendto(request_capital.encode(),serverInfo) # send data to designated server
		input_time = time.time()	# make another time variable due to user's input time
		(capitalized_message, serverAddress) = clientSocket.recvfrom(2048) # wait for recieving data from Server
		print('\nReply from server:', capitalized_message.decode())
		print("Response time : ",round((time.time()-input_time)*1000,1), " ms") # returns elapsed time data from sending data																				# to recieving data
		input_time = 0 # clear time data

	elif message == "2": # return client's ip and port info.
		(client_data, serverAddress) = clientSocket.recvfrom(2048)
		print('\nReply from server:', client_data.decode())
		print("Response time : ",round((time.time()-start_time)*1000,1), " ms")

	elif message == "3": # return server's local datetime
		(TimeMessage, serverAddress) = clientSocket.recvfrom(2048)
		print('\nReply from server: time =',TimeMessage.decode())
		print("Response time : ",round((time.time()-start_time)*1000,1), " ms")

	elif message == "4": # return client request count
		(request_count, serverAddress) = clientSocket.recvfrom(2048)
		print("You've requested function from server for ", request_count.decode(), 
				" times\n\n")
		print("Response time : ",round((time.time()-start_time)*1000,1), " ms")

	elif message == "5" : # exit program with closing client socket
		clientSocket.close()
		print("Bye Bye")
		exit(0)

	elif terminate: # ctrl+c shutdown with closing client socket
		message = "INT"
		clientSocket.sendto(message.encode(),serverInfo)
		clientSocket.close()
		print("Ctrl+C interruption detected \n")
		print("Bye Bye")
		exit(0)

	else: # notify incorrect input 
		print("Invalid Function")


clientSocket.close()
time.sleep(1) # deactivate time function

