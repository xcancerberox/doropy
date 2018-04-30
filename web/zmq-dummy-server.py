import time
import random
import zmq


def producer():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://127.0.0.1:5557")
    # Start your result manager and workers before you start your producers
    while True:
        message = {"metric": "temp", "timestamp": time.time(), "value": random.randint(15, 34)}
        zmq_socket.send_json(message)
        time.sleep(2)
        print(message)

producer()
