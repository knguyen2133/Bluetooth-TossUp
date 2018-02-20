# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *

import socket, time, thread

def serverTx(client_sock):
    try:
        while True:
            sendData = raw_input()
            if len(sendData) == 0: break
            client_sock.send(sendData)

            time.sleep(1)
    except IOError:
        pass

def serverRx(client_sock):
    try:
        while True:
            data = client_sock.recv(1024)
            if len(data) == 0: break
            print("Client: %s" % data)

            time.sleep(1)
    except IOError:
        pass



def serverBt():
    print("You are Server")

    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "Server",
                       service_id = uuid,
                       service_classes = [ uuid, SERIAL_PORT_CLASS ],
                       profiles = [ SERIAL_PORT_PROFILE ],
    #                   protocols = [ OBEX_UUID ]
                        )

    print("Waiting for connection on RFCOMM channel %d" % port)

    socket.setdefaulttimeout(10);
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    try:
        thread.start_new_thread( serverTx, (client_sock))
        thread.start_new_thread( serverRx, (client_sock))
    except:
        print("Unable to start Client Thread")

    print("Disconnected\n\n")

    client_sock.close()
    server_sock.close()
