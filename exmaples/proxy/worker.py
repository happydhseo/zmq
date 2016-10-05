import zmq

import time
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:5560")

while True:
    message = socket.recv()
    print("Received requet: %s" % message)
    time.sleep(1)
    socket.send(b"World")