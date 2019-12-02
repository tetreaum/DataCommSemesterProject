"""
A file to hold the GUI logic and instantiation of the host server. When the user connects to the
CentralServer with the intent to host games it will start a new instance of HostServerThread.
HostServerThread will then create HostServerWorkerThreads as it receives connections from outside.
After Host has created its own HostServer it will then connect to itself through a socket so all
players can be handled the same way.
Run pip install pillow in the command line to access PIL
"""
import tkinter as tk
import tkinter.font
import socket
import pickle
import _thread as _thr
# from network import Network
from PIL import Image
from PIL import ImageTk

HEIGHT = 750
WIDTH = 800

name = ""
myIP = ""
myPort = ""
serverIP = ""
serverPort = ""
server = ""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def threadedClient(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending : ", reply)
            conn.sendall(str.encode(reply))
        except:
            break
    print("Lost connection")
    conn.close


def threadServer(sock, name, myIP, myPort, serverIP, serverPort):
    try:
        sock.bind((myIP, int(myPort)))
        print("socket bound")
    except socket.error as e:
        print(str(e))
    sock.listen(4)
    while True:
        conn, addr = sock.accept()
        print("Connected to: ", addr)
        _thr.start_new_thread(threadedClient, (conn, ))


def connect(name, myIP, myPort, serverIP, serverPort):
    consoleDisplay['text'] = "username: " + name + "\nmyIP: " + myIP + "\nmyPort: " + myPort + "\nserverIP: " + serverIP + "\nserverPort: " + serverPort
    # Connect to central server
    s.connect((serverIP, int(serverPort)))
    # con, addr = s.accept()
    if myIP == "" and myPort == "":
        # TODO: connect to central server and ask it for hosts list, print it to screen
        print("In if")
        # Convert inputs into dictionary
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
                displayText.append(keys + " : " + values + "\n")
                print(keys + " : " + values + "\n")

    else:
        # TODO: connect to central server, tell it we're hosting
        print("I'm hosting, starting server")
        _thr.start_new_thread(threadServer, (s, name, myIP, myPort, serverIP, serverPort, ))
        # TODO: connect to our own server that is running now
        # TODO: in host server thread report back when we have 4 connections
    print("DONE")
    s.close()


def executeCommand(consoleEntry):
    consoleDisplay['text'] = consoleEntry
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
myIPEntry.insert(0, "35.40.26.200")  # TODO: remove the default IP
myIPEntry.place(relx=0.525, rely=0.05, relwidth=0.45, relheight=0.9)

myPortLabel = tk.Label(myPortFrame, font=('Courier', 10), text='Your Host Port: ')
myPortLabel.place(relx=0.025, rely=0.05, relwidth=0.45, relheight=0.9)

myPortEntry = tk.Entry(myPortFrame, font=('Courier', 12))
myPortEntry.insert(0, "5555")  # TODO: remove the default Port
myPortEntry.place(relx=0.525, rely=0.05, relwidth=0.45, relheight=0.9)

serverIPLabel = tk.Label(serverIPFrame, font=('Courier', 10), text='Server IP: ')
serverIPLabel.place(relx=0.025, rely=0.05, relwidth=0.45, relheight=0.9)

serverIPEntry = tk.Entry(serverIPFrame, font=('Courier', 12))
serverIPEntry.insert(0, "35.40.26.200")  # TODO: remove the default IP
serverIPEntry.place(relx=0.525, rely=0.05, relwidth=0.45, relheight=0.9)

serverPortLabel = tk.Label(serverPortFrame, font=('Courier', 10), text='Server Port: ')
serverPortLabel.place(relx=0.025, rely=0.05, relwidth=0.45, relheight=0.9)

serverPortEntry = tk.Entry(serverPortFrame, font=('Courier', 12))
serverPortEntry.insert(0, "12000")  # TODO: remove the default Port
serverPortEntry.place(relx=0.525, rely=0.05, relwidth=0.45, relheight=0.9)

connectButton = tk.Button(connectButtonFrame, text="Connect", font=('Courier', 12), command=lambda: connect(nameEntry.get(), myIPEntry.get(), myPortEntry.get(), serverIPEntry.get(), serverPortEntry.get()))
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
