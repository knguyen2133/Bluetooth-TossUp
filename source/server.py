from bluetooth import *

import time, threading

def serverTxThread(client_sock):
    try:
        while True:
            sendData = raw_input()
            client_sock.send(sendData)
            if sendData == "```":
                break
            time.sleep(1)
    except (IOError, KeyboardInterrupt) as e:
        print("Tx Close")
        pass

def serverRxThread(client_sock):
    try:
        while True:
            data = client_sock.recv(1024)
            if data == "```":
                break
            print("\nClient: %s" % data)

            time.sleep(1)
    except (IOError, KeyboardInterrupt) as e:
        print("Rx Close")
        pass

def serverBt():
    print("You are Server")

    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(.01)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "Server",
                       service_id = uuid,
                       service_classes = [ uuid, SERIAL_PORT_CLASS ],
                       profiles = [ SERIAL_PORT_PROFILE ],
    #                   protocols = [ OBEX_UUID ]
                        )

    print("Waiting for connection on RFCOMM channel %d" % port)

    server_sock.settimeout(7);
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    try:
        serverTx = threading.Thread(target = serverTxThread, args=(client_sock,))
        serverRx = threading.Thread(target = serverRxThread, args=(client_sock,))
        serverTx.start()
        serverRx.start()

    except:
        print("Unable to start Server Thread")

    while True:
        if(False):
            print("1");

    print("Disconnected\n\n")

    client_sock.close()
    server_sock.close()
