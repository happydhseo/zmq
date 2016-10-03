import zmq
from  multiprocessing import Process

def slave():
    # Setup ZMQ.
    context = zmq.Context()
    sock = context.socket(zmq.REQ)
    sock.connect("tcp://localhost:5557")

    while True:
        # Say we're available.
        sock.send_json({"msg": "available"})

        # Retrieve work and run the computation.
        work = sock.recv_json()
        if work == {}:
            continue
        idx = work["idx"]
        data = work["data"]

        result = run_computation(data)
        # We have a result, let's inform the master about that, and receive the
        # "thanks".
        resp = {"msg": "result", "result": result, "idx": idx}
        # print resp
        sock.send_json(resp)
        sock.recv()

def run_computation(data):
    dx = 0.1
    dy = 0.1
    nu = 10.00
    sigma = 0.25
    dt = sigma * dx * dy / nu
    res = data[1][1] + \
          (nu * dt / dx ** 2) * (data[1][2] - 2 * data[1][1] + data[1][0]) + \
          (nu * dt / dy ** 2) * (data[0][1] - 2 * data[1][1] + data[2][1])
    return res

if __name__ == "__main__":
    NUM_SLAVES = 6
    for i in xrange(NUM_SLAVES):
        Process(target=slave).start()
