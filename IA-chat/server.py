import sys
import socket
import select
import time
import hashlib
import random

aliases = ("Sh", "Wnh", "Mnhk", "Khn", "Hngwn", "Jhn")
HOST = raw_input("Host: ")
SOCKETS = {}
logfile = None
SERVER_SOCKET = None
RECV_BUFFER = 2048
PORT = 5000
PASSWORD = "qwerty"


def chatServer():
    global SERVER_SOCKET
    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SERVER_SOCKET.bind((HOST, PORT))
    SERVER_SOCKET.listen(5)
    SOCKETS[SERVER_SOCKET] = ["Server",0]
    print "Server is running on " + str(HOST) + " : " + str(PORT)
    try :
        while 1:
            read,write,error = select.select(SOCKETS.keys(),[],[],0)
            for sock in read:
                if sock == SERVER_SOCKET:
                    sockfd, addr = SERVER_SOCKET.accept()
                    alias = aliases[random.randint(0, len(aliases)-1)]
                    SOCKETS[sockfd] = [alias,0]
                    broadcast(sockfd, "%s joined the chat\n" % alias)
                else:
                    try:
                        alias = SOCKETS[sock][0]
                        data = sock.recv(RECV_BUFFER)
                        if data:
                            if not command(sock,data):
                                broadcast(sock, "\r" + alias + ":" + data)
                        else:
                            if sock in SOCKETS.keys():
                                del SOCKETS[sock]
                                broadcast(sock, "%s is offline\n" % alias)
                    except:
                        broadcast(sock, " %s is offline\n" % alias)
                        continue
    except:
        print "\nConnection closed \n"
        SERVER_SOCKET.close()
    SERVER_SOCKET.close()

def broadcast (sock, message):
    for socket in SOCKETS.keys():
        if socket != SERVER_SOCKET and socket != sock :
            try :
                socket.send(message)
            except:
                socket.close()
                if socket in SOCKETS.keys():
                    del SOCKETS[socket]

def send(sock, alias, message):
    try:
        sock.send("\r" + alias + ": " + message + "\n")
    except:
        sock.close()
        if socket in SOCKETS.keys():
            del SOCKETS[socket]

def checkPassword(sock, pswd):
    global SOCKETS
    if pswd == PASSWORD:
        SOCKETS[sock][1] = 1
        send(sock, SOCKETS[SERVER_SOCKET][0] ,"Access granted")
        return True
    send(sock, SOCKETS[SERVER_SOCKET][0] ,"Wrong password")
    return False


def command(sock, data):
    if "/users" == data.strip():
        message = ""
        for s in SOCKETS:
            if SOCKETS[s][0] == "Server" :
                continue
            if sock == s:
                message+= "[You]"
            if SOCKETS[s][1]:
                message+= "[ADMIN]"
            message += SOCKETS[s][0] + "\n"
        message = message[:len(message)-1]
        send(sock, SOCKETS[SERVER_SOCKET][0] , "\n" + message)
        return True
    if "/alias" in data:
        new = data[7:len(data.strip())]
        if len(new.strip()) > 3:
            old = SOCKETS[sock][0]
            SOCKETS[sock][0] = new
            broadcast(None, "Alias " + old + " was changed. New alias: " +
            SOCKETS[sock][0] + " \n")
            return True
    if "/sticker" in data:
        sticker = data[9:len(data.strip())]
        if len(sticker.strip()) > 0:
            addSticker(sock, sticker)
            return True
    if "/pass" in data:
        pswd = data[6:len(data.strip())]
        if len(pswd.strip()) > 0:
            checkPassword(sock, pswd)
            return True
    if "/exit" == data.strip():
        sock.close()
        del SOCKETS[sock]
    if "/kick" in data and SOCKETS[sock][1] == 1:
        alias = data[6:len(data.strip())]
        if len(alias.strip()) > 0:
            kick(alias)
            return True
    if "/stop" == data.strip() and SOCKETS[sock][1] == 1:
        closeConnection()
        return True
    return False


def kick(alias):
    for sock in SOCKETS:
        if SOCKETS[sock][0] == alias.strip() and sock != SERVER_SOCKET:
            broadcast(None, SOCKETS[sock][0] + " was kicked \n")
            sock.close()
            del SOCKETS[sock]

def addSticker(sock, sticker):
            if sticker == 'omg':
                send(sock, SOCKETS[sock][0], "(@__@)")
            elif sticker == 'lol':
                send(sock, SOCKETS[sock][0], "\nWishes are for free on port 53\n" +
                "           (> ~ <)")
            elif sticker == 'sad':
                send(sock, SOCKETS[sock][0], "(-__-)")
            elif sticker == 'cry':
                send(sock, SOCKETS[sock][0], "(T___T)")
            elif sticker == 'sleep':
                send(sock, SOCKETS[sock][0], "(-.-)Zzz")
            else:
                send(sock, SOCKETS[sock][0], "(^__^)~*")

def closeConnection():
    broadcast(None, "\nConnection closed. Bye-bye \n")
    SERVER_SOCKET.close()

if __name__ == "__main__":
    sys.exit(chatServer())
