import zmq
import time
import random

def worker():
    # set up a zeromq context
    context = zmq.Context()

    # create a pull socket for receiving tasks from the ventilator
    recv_socket = context.socket(zmq.PULL)
    recv_socket.connect("tcp://localhost:6000")

    # create a push socket for sending results to the sink
    sink_socket = context.socket(zmq.PUSH)
    sink_socket.connect("tcp://localhost:6001")

    # receive tasks and send results
    while True:
        data = recv_socket.recv()
        print data
        time.sleep(float(data))
        sink_socket.send(b"python did work: {t}".format(t=data))

if __name__ == '__main__':
    worker()