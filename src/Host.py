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
from PIL import Image
from PIL import ImageTk
from euchre import Euchre

HEIGHT = 750
WIDTH = 800

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = []


def threaded(conn, consoleEntryRef):
    # Update the game state
    consoleDisplay['text'] = conn.recv(4096).decode()


# a helper method to send information easier
def sendMessage(conn, game, message):
    conn[game.turn].send(str.encode(message))


# a helper message to recv information eaiser
# conn.send(str.encode("GameState"))
def recvMessage(conn, game):
    return conn[game.turn].recv(4096).decode()


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
        if player >= 1:  # TODO: set to 4
            # conn.send((str(player)).encode())

            reply = ""
            while True:  # GameLoop
                print("in the game loop")
                try:
                    # If dealing do the dealing stuff
                    if game.dealingPhase:
                        print("Dealing")
                        game.deal()
                        print("dealt")
                        print(game.cards)
                    # If choosing trump let each player choose trump
                    elif game.choosingTrumpPhase1:
                        print("Game.choosingTrumpPhase1")
                        # Send to connections[game.turn] game state
                        sendMessage(connections, game, game.gameStateBuilder(game.turn))
                        # Listen for options
                        option = recvMessage(connections, game)
                        # Report options to game
                        game.pickTrumpStage1(game.turn, option)
                        # If yes, connections[game.dealer] game state
                        if option == "1":
                            game.choosingTrumpPhase1 = False
                            game.discardPhase = True
                            state = game.gameStateBuilder(game.turn)
                            connections[game.dealer].send(state)
                            # connections[game.dealer] options (needs to trade card)
                            option = recvMessage(connections, game)
                            game.discard(game.dealer, option)
                        # Else next person turn
                        else:
                            game.iterateTurn()
                            if game.turn == game.dealer:
                                game.choosingTrumpPhase1 = False
                                game.choosingTrumpPhase2 = True
                    elif game.choosingTrumpPhase2:
                        # Send options to player
                        sendMessage(connections, game, game.gameStateBuilder(game.turn))
                        # Listen for options
                        option = recvMessage(connections, game)
                        # Reprt options to game
                        if option != "4":
                            game.pickTrumpStage2(game.turn, option)
                        else:
                            if game.turn == game.dealer:
                                game.deal()
                            else:
                                game.iterateTurn()
                    # If playing cards have each player play a card
                    elif game.playingCardsPhase:
                        if len(game.moves) == 0:
                            game.newRound()
                            # Send options to player
                            sendMessage(connections, game, game.gameStateBuilder(game.turn))
                            # Listen for options
                            option = recvMessage(connections, game)
                            game.playCard(game.turn, option)
                        else:
                            if game.leader == game.turn:
                                game.scoreTrick(game.moves[game.moves[0]], game.moves[game.moves[1]], game.moves[game.moves[2]], game.moves[game.moves[3]])  # TODO: need to fix order of args given for players
                            else:
                                # Send options to player
                                sendMessage(connections, game, game.gameStateBuilder(game.turn))
                                # Listen for options
                                option = recvMessage(connections, game)
                                game.playCard(game.turn, option)
                        sendMessage(connections, game, game.gameStateBuilder(game.turn))
                        option = recvMessage(connections, game)
                    # Check to see if the game is over after plays.
                    game.checkWinner()
                except:
                    e = sys.exc_info()[0]
                    print(e)
                    break
                # Reporting Phase:
                try:
                    playerCursor = 0
                    for conn in connections:
                        conn.send(str.encode(game.gameStateBuilder(playerCursor)))
                        playerCursor += 1
                except:
                    print("RIPPPPPPPP")
                player = player + 1
        else:
            print("Lost connection")
            conn.close()


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
        else:  # Game specific logic here
            # TODO Create thread to handle server output and listen for new output every 1 second or something like that
            _thr.start_new_thread(threaded, (s, consoleEntry.get(), ))
            # msg = s.recv(4096).decode()
            # print(msg)

    else:
        # # TODO: connect to central server, tell it we're hosting
        # msg = {"name": name, "myIP": myIP, "myPort": myPort, "serverIP": serverIP, "serverPort": serverPort}
        # print("I'm hosting, starting server")
        # serialData = pickle.dumps(msg)
        # s.send(serialData)
        _thr.start_new_thread(threadServer, (s, name, myIP, myPort, serverIP, serverPort, ))
        # TODO: connect to our own server that is running now
        # TODO: in host server thread report back when we have 4 connections


def executeCommand(consoleEntry):
    consoleDisplay['text'] = consoleEntry
    # sendMessage(connections, game, consoleEntry)
    print("DONE2")


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
myIPEntry.insert(0, "localhost")  # TODO: remove the default IP
myIPEntry.place(relx=0.525, rely=0.05, relwidth=0.45, relheight=0.9)

myPortLabel = tk.Label(myPortFrame, font=('Courier', 10), text='Your Host Port: ')
myPortLabel.place(relx=0.025, rely=0.05, relwidth=0.45, relheight=0.9)

myPortEntry = tk.Entry(myPortFrame, font=('Courier', 12))
myPortEntry.insert(0, "5555")  # TODO: remove the default Port
myPortEntry.place(relx=0.525, rely=0.05, relwidth=0.45, relheight=0.9)

serverIPLabel = tk.Label(serverIPFrame, font=('Courier', 10), text='Server IP: ')
serverIPLabel.place(relx=0.025, rely=0.05, relwidth=0.45, relheight=0.9)

serverIPEntry = tk.Entry(serverIPFrame, font=('Courier', 12))
serverIPEntry.insert(0, "localhost")  # TODO: remove the default IP
serverIPEntry.place(relx=0.525, rely=0.05, relwidth=0.45, relheight=0.9)

serverPortLabel = tk.Label(serverPortFrame, font=('Courier', 10), text='Server Port: ')
serverPortLabel.place(relx=0.025, rely=0.05, relwidth=0.45, relheight=0.9)

serverPortEntry = tk.Entry(serverPortFrame, font=('Courier', 12))
serverPortEntry.insert(0, "5555")  # TODO: remove the default Port
serverPortEntry.place(relx=0.525, rely=0.05, relwidth=0.45, relheight=0.9)

connectButton = tk.Button(connectButtonFrame, text="Connect", font=('Courier', 12), command=lambda: connect(nameEntry.get(), myIPEntry.get(), myPortEntry.get(), serverIPEntry.get(), serverPortEntry.get(), consoleEntry.get()))
connectButton.place(relx=0, relheight=1, relwidth=1)

consoleDisplay = tk.Label(consoleFrame, font=('Courier', 12))
consoleDisplay.place(relwidth=1, relheight=0.82)

consoleEntry = tk.Entry(consoleFrame, font=('Courier', 12))
consoleEntry.place(relx=0, rely=0.85, relheight=0.15, relwidth=0.65)

executeButton = tk.Button(consoleFrame, text="Execute", font=('Courier', 12), command=lambda: executeCommand(consoleEntry.get()))
executeButton.place(relx=0.7, rely=0.85, relheight=0.15, relwidth=0.3)
# ===========================GUI Code ends here===========================

# Frames are filled, now running the loop
root.mainloop()
