"""
A file to hold the GUI logic and instantiation of the host server. When the user connects to the
CentralServer with the intent to host games it will start a new instance of HostServerThread.
HostServerThread will then create HostServerWorkerThreads as it receives connections from outside.
After Host has created its own HostServer it will then connect to itself through a socket so all
players can be handled the same way.
Run pip install pillow in the command line to access PIL

This is modeled loosely after both the client and the server in the tutorial here but we did a lot
of the code in here custom ouselves
https://techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
"""
import tkinter as tk
import tkinter.font
import socket
import pickle
import _thread as _thr
import sys
import time
from PIL import Image
from PIL import ImageTk
from euchre import Euchre

HEIGHT = 750
WIDTH = 800

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connections = []


def threaded(conn, consoleEntryRef):
    # Update the game state
    while True:
        consoleDisplay['text'] = conn.recv(4096).decode()


# a helper method to send information easier
def sendMessage(conn, playerNum, message):
    conn[playerNum].send(str.encode(message))


# a helper message to recv information eaiser
# conn.send(str.encode("GameState"))
def recvMessage(conn, playerNum):
    return conn[playerNum].recv(4096).decode()


# THe server's gameLoop and connection logic
def threadServer(sock, name, myIP, myPort, serverIP, serverPort):
    try:
        sock.bind((myIP, int(myPort)))
        print("socket bound")
    except socket.error as e:
        print(str(e))
    print(type(sock))
    sock.listen()
    print("waiting or players, server started")
    connected = set()
    game = Euchre()
    player = 0
    while True:  # Accept connections
        conn, addr = sock.accept()
        game.addPlayer(player)
        player = player + 1
        connections.append(conn)
        print("Connected to: ", addr)
        conn.send(("You are player " + str(player)).encode())
        if player >= 4:
            while True:  # GameLoop
                if game.dealingPhase:
                    game.gameLoop("nothing")
                elif game.playingCardsPhase and len(game.moves) == 0:
                    game.leader = (game.dealer + 1) % 4
                    game.newRound()
                    sendMessage(connections, game.turn, game.gameStateBuilder(game.turn, False))
                    option = recvMessage(connections, game.turn)
                    game.playCard(game.turn, int(option))
                elif game.discardPhase:
                    sendMessage(connections, game.dealer, game.gameStateBuilder(game.dealer, False))
                    option = recvMessage(connections, game.dealer)
                    game.gameLoop(option)
                elif game.gameEnd:
                    pass
                else:
                    try:
                        sendMessage(connections, game.turn, game.gameStateBuilder(game.turn, False))
                        option = recvMessage(connections, game.turn)
                        game.gameLoop(option)
                    except:
                        e = sys.exc_info()[0]
                        print(e)
                        break
                # Reporting Phase:
                try:
                    if not (game.discardPhase or game.dealingPhase):
                        playerCursor = 0
                        for conn in connections:
                            conn.send(str.encode(game.gameStateBuilder(playerCursor, True)))
                            playerCursor += 1
                    else:
                        playerCursor = 0
                        for conn in connections:
                            conn.send(str.encode("The dealer is picking their card"))
                            playerCursor += 1
                except:
                    e = sys.exc_info()[0]
                    print(e)
                    break
                if game.gameEnd:
                    break
        else:
            pass
            # print("Lost connection")
            # conn.close()


def connect(name, myIP, myPort, serverIP, serverPort, consoleInput):
    consoleDisplay['text'] = "username: " + name + "\nmyIP: " + myIP + "\nmyPort: " + myPort + "\nserverIP: " + serverIP + "\nserverPort: " + serverPort
    # con, addr = s.accept()
    if myIP == "" and myPort == "":
        # Connect to server
        s.connect((serverIP, int(serverPort)))
        # Convert inputs into dictionary
        if consoleInput == "":  # Central Server Specific stuff here
            msg = {"name": name, "myIP": myIP, "myPort": myPort, "serverIP": serverIP, "serverPort": serverPort}
            # Serialize the data so we can send it over a socket
            serialData = pickle.dumps(msg)
            s.send(serialData)
            # Receive the list of hosts and display it
            serialList = s.recv(4096)
            listHosts = pickle.loads(serialList)
            displayText = ""
            for item in listHosts:
                for keys, values in item.items():
                    displayText += (keys + " : " + values + "\n")
                    print(keys + " : " + values + "\n")
                    consoleDisplay['text'] = displayText
        else:
            _thr.start_new_thread(threaded, (s, consoleEntry.get(), ))
    else:
        _thr.start_new_thread(threadServer, (s, name, myIP, myPort, serverIP, serverPort, ))

        time.sleep(0.5)

        # Connect to the local server we are hosting
        s2.connect((serverIP, int(serverPort)))
        _thr.start_new_thread(threaded, (s2, consoleEntry.get(), ))


def executeCommand(consoleEntry, myIP, myPort):
    # consoleDisplay['text'] = consoleEntry
    # sendMessage(connections, game, consoleEntry)
    if myIP == "" and myPort == "":
        s.send(str.encode(consoleEntry))
        print("sending stuff to server")
    else:
        s2.send(str.encode(consoleEntry))
        print("sending stuff to server")


# ===========================GUI Code starts here===========================
root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

photoImg = Image.open('BackgroundImage.jpg')
photoImg = photoImg.resize((WIDTH, HEIGHT), Image.ANTIALIAS)

background_image = ImageTk.PhotoImage(photoImg)
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Frames for orgranizing GUI
nameFrame = tk.Frame(root, bg='#80c1ff', bd=5)
nameFrame.place(relx=0.06666, rely=0.05, relwidth=0.4, relheight=0.075)

myIPFrame = tk.Frame(root, bg='#ff0000', bd=5)
myIPFrame.place(relx=0.06666, rely=0.175, relwidth=0.4, relheight=0.075)

myPortFrame = tk.Frame(root, bg='#000000', bd=5)
myPortFrame.place(relx=0.06666, rely=0.3, relwidth=0.4, relheight=0.075)

serverIPFrame = tk.Frame(root, bg='#0000ff', bd=5)
serverIPFrame.place(relx=0.53333, rely=0.05, relwidth=0.4, relheight=0.075)

serverPortFrame = tk.Frame(root, bg='#ffffff', bd=5)
serverPortFrame.place(relx=0.53333, rely=0.175, relwidth=0.4, relheight=0.075)

connectButtonFrame = tk.Frame(root, bg='#00ff00', bd=5)
connectButtonFrame.place(relx=0.53333, rely=0.3, relwidth=0.4, relheight=0.075)

consoleFrame = tk.Frame(root, bg='#80c1ff', bd=10)
consoleFrame.place(relx=0.06666, rely=0.425, relwidth=0.86668, relheight=0.5)

# Filling Frames!
nameLabel = tk.Label(nameFrame, font=('Courier', 12), text='Username: ')
nameLabel.place(relx=0.025, rely=0.05, relwidth=0.45, relheight=0.9)

nameEntry = tk.Entry(nameFrame, font=('Courier', 12))
nameEntry.place(relx=0.525, rely=0.05, relwidth=0.45, relheight=0.9)

myIPLabel = tk.Label(myIPFrame, font=('Courier', 12), text='Your IP: ')
myIPLabel.place(relx=0.025, rely=0.05, relwidth=0.45, relheight=0.9)

myIPEntry = tk.Entry(myIPFrame, font=('Courier', 12))
myIPEntry.place(relx=0.525, rely=0.05, relwidth=0.45, relheight=0.9)

myPortLabel = tk.Label(myPortFrame, font=('Courier', 10), text='Your Host Port: ')
myPortLabel.place(relx=0.025, rely=0.05, relwidth=0.45, relheight=0.9)

myPortEntry = tk.Entry(myPortFrame, font=('Courier', 12))
myPortEntry.place(relx=0.525, rely=0.05, relwidth=0.45, relheight=0.9)

serverIPLabel = tk.Label(serverIPFrame, font=('Courier', 10), text='Server IP: ')
serverIPLabel.place(relx=0.025, rely=0.05, relwidth=0.45, relheight=0.9)

serverIPEntry = tk.Entry(serverIPFrame, font=('Courier', 12))
serverIPEntry.place(relx=0.525, rely=0.05, relwidth=0.45, relheight=0.9)

serverPortLabel = tk.Label(serverPortFrame, font=('Courier', 10), text='Server Port: ')
serverPortLabel.place(relx=0.025, rely=0.05, relwidth=0.45, relheight=0.9)

serverPortEntry = tk.Entry(serverPortFrame, font=('Courier', 12))
serverPortEntry.place(relx=0.525, rely=0.05, relwidth=0.45, relheight=0.9)

connectButton = tk.Button(connectButtonFrame, text="Connect", font=('Courier', 12), command=lambda: connect(nameEntry.get(), myIPEntry.get(), myPortEntry.get(), serverIPEntry.get(), serverPortEntry.get(), consoleEntry.get()))
connectButton.place(relx=0, relheight=1, relwidth=1)

consoleDisplay = tk.Label(consoleFrame, font=('Courier', 12))
consoleDisplay.place(relwidth=1, relheight=0.82)

consoleEntry = tk.Entry(consoleFrame, font=('Courier', 12))
consoleEntry.place(relx=0, rely=0.85, relheight=0.15, relwidth=0.65)

executeButton = tk.Button(consoleFrame, text="Execute", font=('Courier', 12), command=lambda: executeCommand(consoleEntry.get(), myIPEntry.get(), myPortEntry.get()))
executeButton.place(relx=0.7, rely=0.85, relheight=0.15, relwidth=0.3)
# ===========================GUI Code ends here===========================

# Frames are filled, now running the loop
root.mainloop()
