import zmq
import time
import random


def ventilator():
    # set up a zeromq contex
    context = zmq.Context()

    # create a push socket for sending tasks to workers
    send_sock = context.socket(zmq.PUSH)
    send_sock.bind("tcp://*:6000")
    
    # wait for workers to connect... slow joiner syndrome
    time.sleep(1)


    # start the message loop
    for x in xrange(100):
        work = random.random()
        send_sock.send(bytes(str(work)))

if __name__ == '__main__':
    ventilator()
