import socket
import _thread as _th
import pickle
# import threading
# import sys


def Main():
    # list to hold host players
    listHosts = [{"test": "test"}]

    # server and port variables
    server = "35.40.26.200"   # this should be ipv4 address of who's running the server
    port = 12000

    print("started server " + server + " on port " + str(port))

    # Create socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind port to server
    try:
        soc.bind((server, port))
    except socket.error as err:
        print(str(err))

    # Listen for connections
    soc.listen(20)

    def clientThread(con):
        while True:
            # receiving data from client
            data = con.recv(2048)

            if not data:
                print("Disconnected")
                break
            
            # Unpack serialized data
            connectedUser = pickle.loads(data)

            # If user is not host, send them a list of hosts
            if connectedUser["myIP"] == "" and connectedUser["myPort"] == "":
                serialListHosts = pickle.dumps(listHosts)
                con.send(serialListHosts)
            # if user is host, add them to list of hosts
            else:
                listHosts.add(data)
                msg = "You are now hosting on port " + data.get["port"]
                con.send(msg)

        con.close()

    # a while loop until client wants to exit
    while True:
  
        # establish connection with client
        con, addr = soc.accept()
  
        # Start a new thread and return its identifier
        _th.start_new_thread(clientThread, (con,))

    soc.close()


if __name__ == '__main__':
    Main()
