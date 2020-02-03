#! /usr/bin/env python3
import re
import sys
import getopt
import socket
import traceback

from threading import Thread
from control import movement, decoder
from protocol import protocol
from time import sleep

from queue import Queue
from concurrent.futures import ThreadPoolExecutor


message_queue = Queue(maxsize=10)


def command_line():
    while True:
        if not movement.is_motor_connected():
            print("Motor is not connected properly")
            break

        command = input(">")
        message_queue.put_nowait(command)


def server():
    port = 4444  # default port is 4444
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("0.0.0.0", port))
        s.listen(1)
        print("waiting for connections")
        sock = s.accept()[0]
    finally:
        s.close()

    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    print("connection success! ")

    while True:
        while not movement.is_motor_connected():
            print("Motor is not connected properly")
            sleep(10)

        try:
            msg = protocol.receive_message(sock).decode("ascii")  # "F 100 1000"

            if msg == "STOP":  # Urgent stop
                clear_queue()
                movement.stop()
            else:
                print("Pushing message into the queue", msg)
                message_queue.put_nowait(msg)
                print("There are now", message_queue.qsize(), "in the queue")
        except BrokenPipeError:
            print("Peer closed the connection")


def clear_queue():
    while not message_queue.empty():
        print("Cleared", message_queue.get_nowait())
        message_queue.task_done()


def consumer():
    while True:
        try:
            msg = message_queue.get()
            print("Consuming message from the queue", msg)

            decoder.parse_command(msg)
        except Exception as e:
            print("Crashed and burnder", str(e))
            traceback.print_exc()
        finally:
            message_queue.task_done()


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "server":
            producer = server
    else:
        producer = command_line

    with ThreadPoolExecutor(2) as executor:
        [executor.submit(producer), executor.submit(consumer)]


if __name__ == "__main__":
    main()
