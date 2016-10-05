import zmq
import numpy as np
import time

def master(arr, time_steps):
    # Setup ZMQ.
    context = zmq.Context()

    # for sending out work to the workers
    sock = context.socket(zmq.REP)
    sock.bind("tcp://*:10000")

    # for pushing up work to the front end
    pubsub_socket = context.socket(zmq.PUB)
    pubsub_socket.bind("tcp://*:6557")

    # prevents 'slow-joiner' syndrome
    time.sleep(0.2)
    time_step_counter = 0
    while time_step_counter < time_steps:
        print "TIMESTEP =", time_step_counter
        # init an empty arr with same shape for holding results
        results_array = np.zeros(arr.shape)

        # send the arr out to any listeners
        pubsub_socket.send_json({"timestep": time_step_counter, "data": arr.tolist()})

        # Generate the json messages for all computations.
        works = generate_works(arr)

        # How many calculations are expected?
        n_total = arr.size

        # Loop until all results arrived.
        results_count = 0
        while results_count < n_total:
            # Receive;
            j = sock.recv_json()

            # First case: worker says "I'm available". Send him some work.
            if j['msg'] == "available":
                send_work(sock, works)
            elif j['msg'] == "result":
                idx = j["idx"]
                results_count += 1

                results_array[idx[0]][idx[1]] = j["result"] 
                send_thanks(sock)

        # Results are all in.
        print "=== Results are all in ==="
        # now publish on PUB socket
        arr = results_array
        time_step_counter += 1

def send_work(sock, works):
    try:
        wrk = next(works)
        sock.send_json(wrk)
    except StopIteration:
        # no more work to do
        sock.send_json({})


def generate_works(arr):
    # pad the array with zeros to handle edges
    tmp = np.lib.pad(arr, (1, 1), 'constant', constant_values=[0])
    for i in xrange(1, tmp.shape[0] - 1):
        for j in xrange(1, tmp.shape[1] - 1):
            data = tmp[i - 1: i + 2, j - 1: j + 2].tolist()
            wrk = {"idx": [i - 1, j - 1], "data": data}
            yield wrk


def send_thanks(sock):
    sock.send("")

if __name__ == "__main__":
    # start with nada
    init = np.zeros((100, 100))

    init[40:60, 40:60] = 10.0
    init[60:80, 60:80] = 10.0
    master(init, 200)
