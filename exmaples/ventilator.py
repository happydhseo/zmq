import zmq
import time
"""set up a zeromq context"""
context = zmq.Context()

"""create a push socket for sending tasks to workers"""
send_sock = context.socket(zmq.PUSH)
send_sock.bind("tcp://*:9555")
time.sleep(1)

"""start the message loop"""
for x in xrange(100):

    send_sock.send("task: " + str(x))
    # msg = send_sock.recv()
time.sleep(1)