import socket
import threading
from _thread import *
import sys


def Main():
    # Dictionary to hold connected players
    # Entry format is "name:" [ip, hosting port]
    connectedPlayers = {}

    # server and port variables
    server = ""   # this should be ipv4 address of who's running the server
    port = 12000

    # Create socket 
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Bind port to server
    try:
        soc.bind((server, port))
    except socket.error as err:
        str(err)

    # Listen for connections
    soc.listen(4)

    # a while loop until client wants to exit 
    while True: 
  
        # establish connection with client 
        con, addr = soc.accept()
  
        # Start a new thread and return its identifier 
        start_new_thread(client_thread, (con,))

    soc.close()

    def client_thread(con):
        while True:
            # receiving data from client
            data = con.recv(2048)

            if not data:
                print("Disconnected")
                break
            
            # This is where we will call game logic

            con.close()


if __name__ == '__main__': 
    Main() 