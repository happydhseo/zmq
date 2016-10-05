import zmq
import random
import time
import json
import sys

port = sys.argv[1]
context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.bind('tcp://*:{port}'.format(port=port))

# slow joiner prevent
time.sleep(1)

for i in xrange(100):
    zip_code = random.choice([78701, 78702, 78703])
    msg = {"zip": zip_code, "temp": random.randint(60, 100), "port": port}
    pub.send_multipart([bytes(str(zip_code)), bytes(json.dumps(msg))])
    time.sleep(0.5)
