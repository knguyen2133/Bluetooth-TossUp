from bluetooth import *
import sys, time, threading

def clientTxThread(sock):
    try:
        while True:
            sendData = raw_input()
            if len(sendData) == 0: break
            sock.send(sendData)

            time.sleep(1)
    except (IOError, KeyboardInterrupt) as e:
        print("Tx Close")
        pass

def clientRxThread(sock):
    try:
        while True:
            data = sock.recv(1024)
            if len(data) == 0: break
            print("\nServer: %s" % data)

            time.sleep(1)
    except (IOError, KeyboardInterrupt) as e:
        print("Rx Close")
        pass

def clientBt(addr):
    print("You are Client")

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_matches = find_service( uuid = uuid, address = addr )

    if len(service_matches) == 0:
        print("Couldn't find the service")
        return 0

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    print("Connecting to \"%s\" on %s" % (name, host))

    # Create the client socket
    sock=BluetoothSocket( RFCOMM )
    sock.connect((host, port))

    print("Connected")

    try:
        clientTx = threading.Thread(target = clientTxThread, args=(sock,))
        clientRx = threading.Thread(target = clientRxThread, args=(sock,))
        clientTx.start()
        clientRx.start()
    except:
        print("Unable to start Client Thread")
    while True:
        if(False):
            print("1");

    print("Disconnected\n\n")

    sock.close()
