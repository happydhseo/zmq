import zmq
import json

context = zmq.Context()
sub = context.socket(zmq.SUB)
sub.connect("tcp://localhost:8000")
sub.connect("tcp://localhost:8001")

# MUST SET THIS OR ELSE NO MESSAGES!
sub.setsockopt(zmq.SUBSCRIBE, '78702')

while True:
    topic, payload = sub.recv_multipart()
    data = json.loads(payload)
    print topic, data
