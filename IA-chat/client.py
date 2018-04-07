import sys
import socket
import select

def client():
    host = raw_input("Host: ")
    port = 5000
    buf = ''

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()

    print 'Connection established'
    #alias = raw_input("Alias: ")
    #if len(alias.strip())>0:
    #    s.send(alias)
    #else :
    #    print 'Unable to connect'
        #sys.exit()
    sys.stdout.write('Me: '); sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]
        read, write, error = select.select(socket_list , [], [])
        for sock in read:
            if sock == s:
                data = sock.recv(2048)
                if not data :
                    print '\nDisconnected..'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    sys.stdout.write('Me: '); sys.stdout.flush()

            else :
                # user entered a message
                message = sys.stdin.readline()
                buf = message
                if len(message.strip())>0:
                    s.send(message)
                    buf = ''
                sys.stdout.write('Me: '); sys.stdout.flush()

if __name__ == "__main__":
    sys.exit(client())
