import socket
import _thread as _th
# import threading
# import sys


def Main():
    # list to hold host players
    listHosts = []

    # server and port variables
    server = ""   # this should be ipv4 address of who's running the server
    port = 12000

    # Create socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind port to server
    try:
        soc.bind((server, port))
    except socket.error as err:
        str(err)

    # Listen for connections
    soc.listen(4)

    def client_thread(con):
        while True:
            # receiving data from client
            data = con.recv(2048)

            if not data:
                print("Disconnected")
                break
            
            # Add host to list of hosts
            if data.get["isHost"] is True:
                listHosts.add(data)
                msg = "You are now hosting on port " + data.get["port"]
                con.send(msg)
            else:
                con.send(listHosts)

            con.close()

    # a while loop until client wants to exit
    while True:
  
        # establish connection with client
        con, addr = soc.accept()
  
        # Start a new thread and return its identifier
        _th.start_new_thread(client_thread, (con,))

    soc.close()


if __name__ == '__main__':
    Main()
