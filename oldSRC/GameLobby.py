"""
Basic socket programming in python. I used this website as a tutorial.
https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
Server takes client input, reverses it, and sends it back.
"""
# import socket programming library
import socket
import _thread as thread
# import thread module

import threading

print_lock = threading.Lock()

# thread fuction


def threaded(c):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('Client Disconnected')
            # lock released on exit
            print_lock.release()
            break

        # reverse the given string from client
        data = data[::-1]

        # send back reversed string to client
        c.send(data)

    # connection closed
    c.close()


def Main():
    host = ""

    # Port number, bind socket to port
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a while loop until client wants to exit
    while True:

        # establish connection with client
        c, addr = s.accept()

        # Creat arrays for ListHosts and FileLists
        listHost = []
        fileLists = []

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        # start_new_thread(threaded, (c,), listHost, fileLists)
        thread.start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
