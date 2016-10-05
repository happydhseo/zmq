import zmq
import random
import time
import json

context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.bind('tcp://*:8000')

# slow joiner prevent
time.sleep(1)

for i in xrange(100):
    zip_code = random.choice([78701, 78702, 78703])
    msg = {"zip": zip_code, "temp": random.randint(60, 100)}
    pub.send(json.dumps(msg))
    print msg
    time.sleep(0.5)