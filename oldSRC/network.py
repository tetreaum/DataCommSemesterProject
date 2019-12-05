"""
This is a class to handle all of our connections. Each client will use this to talk to the
server and it abstracts a lot of the socket logic out of the Host and CentralServer files.
We followed this tutorial for how to implement our game since our game is similar in how
the connections would need to be used as it is a turn based game.
https://techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
"""
import socket
import pickle


class Network:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip  # change to your own IP (maybe make this an arg later)
        self.port = port
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048 * 2))
        except socket.error as e:
            print(e)
