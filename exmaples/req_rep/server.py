import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:5555")

while True:
    message = socket.recv()
    print "Received request: {msg}".format(msg=message)
    socket.send('World')

socket.close()
context.term()
