# # # # # # # # # # # #  #
# ChatTCPServer.py       #
# 20124602 Lee Sueng Jun #
# # # # # # # # # # # #  #

# Import libraries
from socket import *
from threading import Lock, Thread, Timer
from signal import *
import time
import datetime

buff = 2048

def Check_same_name(name): # check whether requested name already exists in registered name or not
    for names in client_name:
        if name == names:
            return True
        else:
            return False

def Check_special_char(name): # check whether requested name contains special-character or not
    for namealp in name:
        if namealp < 'a' or namealp > 'z':
            return True
            break
        if namealp < 'A' or namealp > 'z':
            return True
            break
        else:
            pass

    return False

def Signal_handling(signum, frame): # ctrl+c event handler
    print("CTRL+C detected \n Bye Bye!!")
    try:
        connectionSocket.close()
        serverSocket.close()
        print("Sockets are now closed")
        exit(0)
    except NameError:   # exception for closing non-existing sockets
        print("No Connection has been made")
        exit(0)

# Class of Multi-thread connection
class ClientHandler(Thread):
    count = 0
    client_list = []
    def __init__(self, name, address, port, socket, lock):   # initialize values for each registered clients
        Thread.__init__(self)
        self.name = name
        self.address = address
        self.port = port
        self.socket = socket
        self.lock = lock
        ClientHandler.count += 1 # total number of clients connected to the server

    # Define functions which are the connected socket thread will performs.
    def run(self):
        welcome = "Welcome {}  !!\nYou've connected to CAU-CSE chat room at ({}). " \
                  "\nYou're <{}>th client" \
            .format(self.name, serverSocket.getsockname(), ClientHandler.count)
        message = ""
        self.socket.send(welcome.encode())
        request_number = 0
        print("Client", self.name, " Connected. Number of connected clients : ", ClientHandler.count)
        while True:
            check_msg = ""
            check_msg = self.socket.recv(buff).decode()
            message = ""
            message = "\n{} > {}".format(self.name, check_msg)
            try: # send message to all except command message
                if check_msg[0] != "/":
                    request_number += 1
                    for clients in threads:
                        if clients.name != self.name:
                            clients.socket.send(message.encode())
                        else:
                            pass
            except IndexError: # client ends connection with ctrl+c while entering message
                ClientHandler.count -= 1
                quit_msg = "\nClient {} , Disconnected. Number of connected clients : {}".format(self.name,
                                                                                                 ClientHandler.count)
                print("Client", self.name, "Disconnected via CTRL+C. Number of connected clients : ",
                      ClientHandler.count)
                for clients in threads:
                    if clients.name != self.name:
                        clients.socket.send(quit_msg.encode())
                    else:
                        pass
                client_name.remove(self.name)
                threads.remove(self)
                break

            if check_msg == "/command":
                message = "\n--------------------\n" \
                          " Chat room commands\n " \
                          "--------------------\n" \
                          "/list : show the list of all users\n" \
                          "/w <nickname> <message> : whisper to <nickname>\n" \
                          "/quit : disconnect from server and quit\n" \
                          "/ver : show server's software version & client software server\n" \
                          "/change <nickname> : change my nickname \n" \
                          "/stats : show stats of how many you've sent and recieve"
                self.socket.send(message.encode())

            if check_msg == "/quit":
                ClientHandler.count -= 1
                quit_msg = "\nClient {} , Disconnected. Number of connected clients : {}".format(self.name,
                                                                                                 ClientHandler.count)
                print("Client", self.name, "Disconnected via quit command. Number of connected clients : ",
                      ClientHandler.count)
                for clients in threads:
                    if clients.name != self.name:
                        clients.socket.send(quit_msg.encode())
                    else:
                        pass
                client_name.remove(self.name)
                threads.remove(self)
                break


            if check_msg == "/stats":
                message = "Total {} messages sent and recieved".format(request_number)
                self.socket.send(message.encode())

            if check_msg == "/ver":
                version = 1.0
                message = "\nSocket Chatting Program Server version : {}".format(version)
                self.socket.send(message.encode())




def Print_Num_of_Client():  # function for printing number of clients
    print("Number of connected clients :", ClientHandler.count)
    Timer(60.0, Print_Num_of_Client).start() # restart the timer

# Main
signal(SIGINT, Signal_handling)  # ctrl+c detection
threads = []            # activated thread list
thread_lock = Lock()  # Lock for each threads, preventing crush between thread and thread

client_name = []

serverPort = 24602  # 34602,44602,54602
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
serverSocket.bind(('', serverPort))

print("The server is ready to receive on port", serverPort)
print("Press(Ctrl+C) to close the server")
Timer(60.0, Print_Num_of_Client).start()  # repeats number of client per 60 seconds


while True:
    try:
        serverSocket.listen(1)
        (connectionSocket, clientAddress) = serverSocket.accept()
        name_message = ""
        name_message = connectionSocket.recv(buff)
        welcome_msg = ""
        name = name_message.decode()

        if len(name) > 64: # exception for over-used name length
            welcome_msg = "1"
            connectionSocket.send(welcome_msg.encode())
            connectionSocket.close()

        elif len(threads) >= 8: # exception for capacity of chat room
            welcome_msg = "2"
            connectionSocket.send(welcome_msg.encode())
            connectionSocket.close()

        elif Check_same_name(name): # exception for duplicated nickname
            welcome_msg = "3"
            connectionSocket.send(welcome_msg.encode())
            connectionSocket.close()

        elif Check_special_char(name): # exception for special-character contained nickname
            welcome_msg = "4"
            connectionSocket.send(welcome_msg.encode())
            connectionSocket.close()

        elif name == "": # exception for aborted connection
            print("Connection aborted")
            connectionSocket.close()

        else: # no problem with nickname and start chatting
            client_name.append(name)
            newThread = ClientHandler(name, clientAddress[0], clientAddress[1], connectionSocket, thread_lock)
            welcome_msg = "0"
            connectionSocket.send(welcome_msg.encode())
            threads.append(newThread)
            newThread.start()


    except ConnectionAbortedError:
        print("Connection aborted")




connectionSocket.close()
serverSocket.close()
print("Close called")