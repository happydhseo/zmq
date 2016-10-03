import zmq
import time
context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.bind("tcp://*:5555")

#  Do 10 requests, waiting each time for a response
for request in xrange(10):
    socket.send("Hello")
    message = socket.recv()
    print "Received reply %s [ %s ]" % (request, message)
    time.sleep(1)

socket.close()
context.term()
