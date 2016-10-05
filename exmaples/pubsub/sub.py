import zmq
import json

context = zmq.Context()
sub = context.socket(zmq.SUB)
sub.connect("tcp://localhost:8000")
sub.setsockopt(zmq.SUBSCRIBE, '')

while True:
    msg = sub.recv()
    print msg