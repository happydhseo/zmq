import zmq
import time
import random
import json

"""task worker function"""
def worker(data):
    return 1


"""set up a zeromq context"""
context = zmq.Context()

"""create a pull socket for receiving tasks from the ventilator"""
recv_socket = context.socket(zmq.PULL)
recv_socket.connect("tcp://localhost:9555")

# """create a push socket for sending results to the sink"""
# sink_socket = context.socket(zmq.PUSH)
# sink_socket.connect("tcp://localhost:9556")

"""receive tasks and send results"""
while True:
    data = recv_socket.recv()
    print data
    # resp = json.dumps(worker(data))
    time.sleep(random.random())
    # recv_socket.send()
    # sink_socket.send(resp)
    # sink_socket.recv()
