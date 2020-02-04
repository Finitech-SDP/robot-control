#! /usr/bin/env python3

import logging
import socket
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

import config
from control import decoder, movement
from protocol import protocol
from util import util

logging.basicConfig(level=config.LOGGING_LEVEL, format=config.LOGGING_FORMAT)

MESSAGE_QUEUE = Queue(maxsize=config.CONTROL_QUEUE_SIZE)


def cli():
    while True:
        movement.exit_if_motors_not_connected()

        command = input(">")

        if command == "STOP":  # Kill-switch
            clear_queue()
            movement.stop()
        else:
            MESSAGE_QUEUE.put_nowait(command)


def server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((config.TCP_HOST, config.TCP_PORT))
            s.listen(backlog=1)
            logging.info(
                "Listening on %s:%d, use ctrl+c to stop",
                util.get_ip(),
                config.TCP_PORT
            )
            sock, addr = s.accept()

            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            with sock:
                while True:
                    movement.exit_if_motors_not_connected()

                    try:
                        msg = protocol.receive_message(sock).decode("ascii")

                        if msg == "STOP":  # Kill-switch
                            clear_queue()
                            movement.stop()
                        else:
                            MESSAGE_QUEUE.put_nowait(msg)
                    except BrokenPipeError:
                        print("Peer closed the connection")
                        break
    except Exception:
        print("SERVER ERROR")
        traceback.print_exc()


def clear_queue():
    while not MESSAGE_QUEUE.empty():
        MESSAGE_QUEUE.get_nowait()
        MESSAGE_QUEUE.task_done()


def consumer():
    while True:
        try:
            msg = MESSAGE_QUEUE.get()

            decoder.parse_command(msg)
        except Exception as e:
            logging.error("Consumer error: %s", str(e))
            traceback.print_exc()
        finally:
            MESSAGE_QUEUE.task_done()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        producer = server
    else:
        producer = cli

    # TODO: handle keyboard interrupts
    with ThreadPoolExecutor(2) as executor:
        executor.submit(producer)
        executor.submit(consumer)


if __name__ == "__main__":
    main()
